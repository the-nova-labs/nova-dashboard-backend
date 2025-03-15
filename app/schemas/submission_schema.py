from pydantic import BaseModel
from typing import List

class NeuronBase(BaseModel):
    hotkey: str


class CompetitionBase(BaseModel):
    target_protein: str
    anti_target_protein: str
    epoch_number: int


class SubmissionBase(BaseModel):
    neuron: NeuronBase
    block_number: int
    score: float
    molecule: str


class MinerSubmissionsRequest(BaseModel):
    competition: CompetitionBase
    submissions: List[SubmissionBase]
