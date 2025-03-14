from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.schemas.submission_schema import MinerSubmissionsRequest
from app.models.crud import get_or_create_competition, get_or_create_neuron, create_submission
from app.models.models import Submission, Neuron, Competition


def submit_results(data: MinerSubmissionsRequest, db: Session):
    """Handles miner submissions, ensuring competitions and neurons exist."""

    competition = get_or_create_competition(db, data.competition.epoch_number, data.competition.protein)
    for submission in data.submissions:
        neuron = get_or_create_neuron(db, submission.neuron.hotkey)
        create_submission(db, competition.id, neuron.id, submission.block_number, submission.score)

    db.commit() 
    return {"message": "Submissions successfully recorded"}


def get_leaderboard(db: Session, epoch_number: int):
    """Fetch miners sorted by max score, then block number, then submission ID, ensuring unique neurons."""

    competition = db.query(Competition).filter_by(epoch_number=epoch_number).first()
    if not competition:
        return []

    # Subquery: Get max score per neuron
    max_scores_subquery = (
        db.query(
            Submission.neuron_id,
            func.max(Submission.score).label("max_score")
        )
        .filter(Submission.competition_id == competition.id)
        .group_by(Submission.neuron_id)
        .subquery()
    )

    # Main query: Fetch only the best submission per neuron based on sorting rules
    leaderboard = (
        db.query(
            Neuron.hotkey,
            Submission.block_number,
            Submission.score.label("max_score")
        )
        .join(Submission, Submission.neuron_id == Neuron.id)
        .join(max_scores_subquery, and_(
            Submission.neuron_id == max_scores_subquery.c.neuron_id,
            Submission.score == max_scores_subquery.c.max_score  # Ensure we only fetch the best score
        ))
        .filter(Submission.competition_id == competition.id)
        .order_by(
            Submission.score.desc(),      # 1️⃣ Highest score first
            Submission.block_number.asc(), # 2️⃣ If tied, lower block number first
            Submission.id.asc()           # 3️⃣ If still tied, smaller submission ID first
        )
        .all()
    )

    # Ensure only one submission per neuron (SQLite-compatible)
    seen_neurons = set()
    filtered_leaderboard = []
    for hotkey, block_number, max_score in leaderboard:
        if hotkey not in seen_neurons:
            filtered_leaderboard.append({"hotkey": hotkey, "block_number": block_number, "max_score": max_score})
            seen_neurons.add(hotkey)  # Avoid duplicates

    return filtered_leaderboard


def get_competition_list(db: Session):
    """Fetch all competitions."""
    return db.query(Competition).order_by(Competition.epoch_number.desc()).all()

