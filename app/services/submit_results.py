from sqlalchemy.orm import Session
from app.schemas.submission_schema import MinerSubmissionsRequest
from app.models.crud import get_or_create_competition, get_or_create_neuron, create_submission


def submit_results(data: MinerSubmissionsRequest, db: Session):
    """Handles miner submissions, ensuring competitions and neurons exist."""

    competition = get_or_create_competition(db, data.competition.epoch_number, data.competition.protein)
    for submission in data.submissions:
        neuron = get_or_create_neuron(db, submission.neuron.hotkey)
        create_submission(db, competition.id, neuron.id, submission.block_number, submission.score)

    db.commit() 
    return {
        "success": True,
    }
