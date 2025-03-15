from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import (
    submit_results, 
    get_leaderboard, 
    get_competition_list,
)
from app.schemas.submission_schema import MinerSubmissionsRequest


router = APIRouter()


@router.post("/submit_results")
def handle_submit_results(data: MinerSubmissionsRequest, db: Session = Depends(get_db)):
    return submit_results(data, db)


@router.get("/leaderboard")
def leaderboard(epoch_number: int, db: Session = Depends(get_db)):
    leaderboard = get_leaderboard(db, epoch_number)
    if leaderboard is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    return leaderboard


@router.get("/competitions")
def get_competitions(db: Session = Depends(get_db)):
    return get_competition_list(db)