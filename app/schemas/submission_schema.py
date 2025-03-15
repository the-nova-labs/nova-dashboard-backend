from pydantic import BaseModel
from typing import List

class NeuronBase(BaseModel):
    hotkey: str


class CompetitionBase(BaseModel):
    protein: str
    epoch_number: int


class SubmissionBase(BaseModel):
    neuron: NeuronBase
    block_number: int
    score: float


class MinerSubmissionsRequest(BaseModel):
    competition: CompetitionBase
    submissions: List[SubmissionBase]
