from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.models import Submission, Neuron, Competition, Challenge        


def get_leaderboard(db: Session, epoch_number: int):
    """Fetch miners sorted by max score, then block number, then submission ID, ensuring unique neurons."""

    competition, protein = (
        db.query(Competition, Challenge.protein)
        .join(Challenge, Challenge.id == Competition.challenge_id)
        .filter(Competition.epoch_number == epoch_number)
        .first()
    )
    print(competition, protein)
    if not competition:
        return []

    leaderboard = (
        db.query(
            Submission.neuron_id,
            Submission.block_number,
            func.max(Submission.score).label("max_score"),
            Neuron.hotkey
        )
        .join(Neuron, Submission.neuron_id == Neuron.id)
        .filter(Submission.competition_id == competition.id)
        .group_by(
            Submission.neuron_id
        ).order_by(
            Submission.score.desc(),
            Submission.block_number.asc(),
            Submission.id.asc()
        ).all()
    )

    return {
        "leaderboard": [
            {
                "hotkey": row.hotkey,
                "block_number": row.block_number,
                "max_score": row.max_score
            }
            for row in leaderboard
        ],
        "competition": {
            "id": competition.id,
            "epoch_number": competition.epoch_number,
            "protein": protein
        }
    }

