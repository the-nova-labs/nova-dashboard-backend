from sqlalchemy.orm import Session
from app.schemas.submission_schema import MinerSubmissionsRequest
from app.models.crud import get_or_create_competition, get_or_create_neuron, create_submission


def submit_results(data: MinerSubmissionsRequest, db: Session):
    """Handles miner submissions, ensuring competitions and neurons exist."""

    submissions = data.submissions
    unique_hotkeys = len({submission.neuron.hotkey for submission in submissions})
    best_submission = min(
        submissions,
        key=lambda x: (-x.score, x.block_number)
    )
    competition_metadata = {
        "unique_hotkeys": unique_hotkeys,
        "best_hotkey": best_submission.neuron.hotkey,
        "best_molecule": best_submission.molecule,
        "best_score": best_submission.score,
    }

    competition = get_or_create_competition(
        db, 
        data.competition.epoch_number, 
        data.competition.target_protein, 
        data.competition.anti_target_protein,
        competition_metadata,
    )
    
    for submission in data.submissions:
        neuron = get_or_create_neuron(db, submission.neuron.hotkey)
        create_submission(
            db, 
            competition.id, 
            neuron.id, 
            submission.block_number, 
            submission.score, 
            submission.molecule,
        )

    db.commit() 
    return {
        "success": True,
    }
