from sqlalchemy.orm import Session
from app.models.models import Competition, Challenge        


def get_competition_list(db: Session):
    """Fetch all competitions."""
    competitions = (
        db.query(Competition, Challenge.protein)
        .join(Challenge, Challenge.id == Competition.challenge_id)  # Join with Challenge table
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