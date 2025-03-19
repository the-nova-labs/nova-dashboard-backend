from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.constants import API_TOKEN
from app.core.database import get_db
from app.services import (
    submit_results, 
    get_leaderboard, 
    get_competition_list,
    get_smiles,
)
from app.schemas.submission_schema import MinerSubmissionsRequest


router = APIRouter()


@router.post("/submit_results")
def handle_submit_results(
    data: MinerSubmissionsRequest, 
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
        
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
        
    api_token = authorization.split(" ")[1]
    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    
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


@router.get("/molecule")
def get_molecule(molecule: str):
    return get_smiles(molecule)
