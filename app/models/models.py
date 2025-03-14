from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List


class Base(DeclarativeBase):
    pass


class Neuron(Base):
    __tablename__ = "neurons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hotkey: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    target_protein: Mapped[str] = mapped_column(String, nullable=False, index=True)
    anti_target_protein: Mapped[str] = mapped_column(String, nullable=False, index=True)
    
class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    challenge_id: Mapped[int] = mapped_column(Integer, ForeignKey("challenges.id"), nullable=False)
    epoch_number: Mapped[int] = mapped_column(Integer, nullable=False)

    challenge: Mapped["Challenge"] = relationship()
    submissions: Mapped[List["Submission"]] = relationship(back_populates="competition")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    block_number: Mapped[int] = mapped_column(Integer, nullable=False)
    competition_id: Mapped[int] = mapped_column(Integer, ForeignKey("competitions.id"), nullable=False)
    neuron_id: Mapped[int] = mapped_column(Integer, ForeignKey("neurons.id"), nullable=False)
    molecule: Mapped[str] = mapped_column(String, nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)

    neuron: Mapped["Neuron"] = relationship()
    competition: Mapped["Competition"] = relationship()
