from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import (
    Competition, 
    Neuron, 
    Protein, 
    Submission,
    CompetitionMetadata,
)


def create_record(session: Session, model_class, **kwargs):
    """Generic function to create and return a database record."""
    try:
        record = model_class(**kwargs)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except SQLAlchemyError as e:
        session.rollback()
        return None


def get_or_create_protein(db: Session, protein: str) -> Protein:
    """Fetch an existing challenge or create a new one if not found."""
    challenge = db.query(Protein).filter_by(protein=protein).first()
    if not challenge:
        challenge = create_record(db, Protein, protein=protein)
    return challenge


def get_or_create_competition(
    db: Session, 
    epoch_number: int, 
    target_protein: str, 
    anti_target_protein: str,
) -> Competition:
    """Fetch an existing competition or create a new one if not found."""
    competition = db.query(Competition).filter_by(epoch_number=epoch_number).first()
    
    if not competition:
        target_protein = get_or_create_protein(db, target_protein)
        anti_target_protein = get_or_create_protein(db, anti_target_protein)
        competition = create_record(
            db, 
            Competition, 
            epoch_number=epoch_number, 
            target_protein_id=target_protein.id, 
            anti_target_protein_id=anti_target_protein.id,
        )
    return competition


def create_competition_metadata_if_not_exists(
    db: Session, 
    competition_id: int, 
    competition_metadata: dict
) -> CompetitionMetadata:
    """Create a new competition metadata record."""
    metadata = db.query(CompetitionMetadata).filter_by(competition_id=competition_id).first()
    if not metadata:
        metadata = create_record(
            db, 
            CompetitionMetadata, 
            competition_id=competition_id, 
            **competition_metadata,
        )
    return metadata


def get_or_create_neuron(db: Session, hotkey: str) -> Neuron:
    """Fetch an existing neuron or create a new one if not found."""
    neuron = db.query(Neuron).filter_by(hotkey=hotkey).first()
    
    if not neuron:
        neuron = create_record(
            db, 
            Neuron, 
            hotkey=hotkey,
        )

    return neuron


def create_submission(db: Session, competition_id: int, neuron_id: int, block_number: int, score: float, molecule: str) -> Submission:
    """Create a new submission record."""
    submission = create_record(
        db, 
        Submission, 
        competition_id=competition_id, 
        neuron_id=neuron_id, 
        block_number=block_number, 
        score=score,
        molecule=molecule,
    )
    return submission


