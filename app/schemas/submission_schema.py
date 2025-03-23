from pydantic import BaseModel, Field
from typing import List, Optional


class NeuronBase(BaseModel):
    hotkey: str


class CompetitionBase(BaseModel):
    target_proteins: List[str]
    anti_target_proteins: List[str]
    epoch_number: int


class SubmissionBase(BaseModel):
    neuron: NeuronBase
    block_number: int
    score: float
    molecule: Optional[str] = None


class MinerSubmissionsRequest(BaseModel):
    competition: CompetitionBase
    submissions: List[SubmissionBase]
