from sqlalchemy.orm import Session, aliased, selectinload, joinedload
from app.models.models import Competition, Protein, Submission
from app.core.metagraph import METAGRAPH


def get_competition_list(db: Session):
    """Fetch all competitions along with their target and anti-target proteins."""

    competitions = (
        db.query(Competition)
        .options(selectinload(Competition.best_submission).selectinload(Submission.neuron))
        .options(joinedload(Competition.target_proteins))  # Load multiple target proteins
        .options(joinedload(Competition.anti_target_proteins))  # Load multiple anti-target proteins
        .order_by(Competition.epoch_number.desc())
        .all()
    )
    json_competitions = [
        {
            "id": competition.id, 
            "epoch_number": competition.epoch_number, 
            "target_proteins": [protein.protein for protein in competition.target_proteins],  
            "anti_target_proteins": [protein.protein for protein in competition.anti_target_proteins],  
            "best_submission":  {
                "hotkey": competition.best_submission.neuron.hotkey,
                "uid": METAGRAPH.get_uid(competition.best_submission.neuron.hotkey) if competition.best_submission.neuron.hotkey else None,
                "score": competition.best_submission.score,
                "block_number": competition.best_submission.block_number,
            } if competition.best_submission else None
        } 
        for competition in competitions
    ]
    
    return {
        "block": METAGRAPH.get_block(),
        "competitions": json_competitions
    }
    
