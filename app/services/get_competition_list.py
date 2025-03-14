from sqlalchemy.orm import Session
from app.models.models import Competition, Protein        


def get_competition_list(db: Session):
    """Fetch all competitions."""
    competitions = (
        db.query(Competition, Protein.target_protein)
        .join(Protein, Protein.id == Competition.challenge_id)  # Join with Challenge table
        .order_by(Competition.epoch_number.desc())  # Sort by epoch_number
        .all()
    )
    return [
        {
            "id": competition.id, 
            "epoch_number": competition.epoch_number, 
            "protein": protein,
        } 
        for competition, protein in competitions
    ]