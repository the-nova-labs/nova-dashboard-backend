from sqlalchemy.orm import Session, aliased, joinedload
from sqlalchemy.sql import func, desc, select
from app.core.metagraph import METAGRAPH
from app.models.models import Submission, Neuron, Competition, Protein        


def get_leaderboard(db: Session, epoch_number: int):
    """Fetch miners sorted by max score, then block number, then submission ID, ensuring unique neurons."""
    competition = (
        db.query(Competition)
        .options(
            joinedload(Competition.target_proteins),
            joinedload(Competition.anti_target_proteins),
        )
        .filter(Competition.epoch_number == epoch_number)
        .first()
    )
    if not competition:
        return None

    # Window function for ranking
    rank_criteria = func.row_number().over(
        partition_by=Submission.neuron_id,
        order_by=[
            desc(Submission.score),
            Submission.block_number,
            Submission.id
        ]
    )

    # Subquery
    subq = (
        select(
            Submission,
            rank_criteria.label('rn')
        )
        .where(Submission.competition_id == competition.id)
        .subquery()
    )

    bs = aliased(Submission, subq)

    # Main query
    stmt = (
        select(
            bs.neuron_id,
            Neuron.hotkey,
            bs.molecule,
            bs.score,
            bs.block_number,
            bs.id,
        )
        .join(Neuron, bs.neuron_id == Neuron.id)
        .where(subq.c.rn == 1)
        .order_by(
            desc(bs.score),
            bs.block_number,
            bs.id
        )
    )

    leaderboard = db.execute(stmt).all()

    return {
        "leaderboard": [
            {
                "hotkey": row.hotkey,
                "block_number": row.block_number,
                "molecule": row.molecule,
                "max_score": row.score,
                "uid": METAGRAPH.get_uid(row.hotkey),
            }
            for row in leaderboard
        ],
        "competition": {
            "id": competition.id,
            "epoch_number": competition.epoch_number,
            "target_proteins": [protein.protein for protein in competition.target_proteins],
            "anti_target_proteins": [protein.protein for protein in competition.anti_target_proteins],
        }
    }

