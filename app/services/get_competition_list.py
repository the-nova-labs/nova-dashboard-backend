from sqlalchemy.orm import Session
from app.models.models import Competition, Protein        


def get_competition_list(db: Session):
    """Fetch all competitions along with their target and anti-target proteins."""
    
    competitions = (
        db.query(
            Competition.id,
            Competition.epoch_number,
            Protein.protein.label("target_protein"),
            Protein.protein.label("anti_target_protein")
        )
        .join(Protein, Protein.id == Competition.target_protein_id)  # Join target protein
        .join(Protein, Protein.id == Competition.anti_target_protein_id)  # Join anti-target protein
        .order_by(Competition.epoch_number.desc())  # Sort by latest epoch first
        .all()
    )

    return [
        {
            "id": competition.id, 
            "epoch_number": competition.epoch_number, 
            "target_protein": competition.target_protein,
            "anti_target_protein": competition.anti_target_protein,
        } 
        for competition in competitions
    ]
