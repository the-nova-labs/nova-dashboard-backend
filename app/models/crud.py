from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import (
    Competition, 
    Neuron, 
    Challenge, 
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


def get_or_create_challenge(db: Session, protein: str) -> Challenge:
    """Fetch an existing challenge or create a new one if not found."""
    challenge = db.query(Challenge).filter_by(protein=protein).first()
    if not challenge:
        challenge = create_record(db, Challenge, protein=protein)
    return challenge


def get_or_create_competition(db: Session, epoch_number: int, protein: str) -> Competition:
    """Fetch an existing competition or create a new one if not found."""
    competition = db.query(Competition).filter_by(epoch_number=epoch_number).first()
    
    if not competition:
        challenge = get_or_create_challenge(db, protein)
        competition = create_record(db, Competition, epoch_number=epoch_number, challenge_id=challenge.id)

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


def create_submission(db: Session, competition_id: int, neuron_id: int, block_number: int, score: float) -> Submission:
    """Create a new submission record."""
    submission = create_record(
        db, 
        Submission, 
        competition_id=competition_id, 
        neuron_id=neuron_id, 
        block_number=block_number, 
        score=score,
    )
    return submission
