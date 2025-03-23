from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.models.models import (
    Competition, 
    Neuron, 
    Protein, 
    Submission,
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


def get_or_create_protein(db: Session, name: str) -> Protein:
    """Fetch an existing protein or create a new one if not found."""
    protein = db.query(Protein).filter_by(name=name).first()
    if not protein:
        protein = create_record(db, Protein, name=name)
    return protein


def get_or_create_competition(
    db: Session, 
    epoch_number: int, 
    target_proteins: List[str], 
    anti_target_proteins: List[str],
) -> Competition:
    """Fetch an existing competition or create a new one if not found."""
    competition = db.query(Competition).filter_by(epoch_number=epoch_number).first()
    
    if not competition:
        target_proteins = [get_or_create_protein(db, p) for p in target_proteins]
        anti_target_proteins = [get_or_create_protein(db, p) for p in anti_target_proteins]
        competition = create_record(
            db, 
            Competition, 
            epoch_number=epoch_number, 
            target_proteins=target_proteins, 
            anti_target_proteins=anti_target_proteins,
        )
    return competition


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


