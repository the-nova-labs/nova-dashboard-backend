from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List


class Base(DeclarativeBase):
    pass


class Neuron(Base):
    __tablename__ = "neurons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hotkey: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)


class Protein(Base):
    __tablename__ = "proteins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    protein: Mapped[str] = mapped_column(String, index=True)

    
class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    target_protein_id: Mapped[int] = mapped_column(Integer, ForeignKey("proteins.id"), nullable=False)
    anti_target_protein_id: Mapped[int] = mapped_column(Integer, ForeignKey("proteins.id"), nullable=False)
    epoch_number: Mapped[int] = mapped_column(Integer, nullable=False)

    target_protein: Mapped["Protein"] = relationship()
    anti_target_protein: Mapped["Protein"] = relationship()
    submissions: Mapped[List["Submission"]] = relationship(back_populates="competition")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    block_number: Mapped[int] = mapped_column(Integer, nullable=False)
    competition_id: Mapped[int] = mapped_column(Integer, ForeignKey("competitions.id"), nullable=False)
    neuron_id: Mapped[int] = mapped_column(Integer, ForeignKey("neurons.id"), nullable=False)
    molecule: Mapped[str] = mapped_column(String)
    score: Mapped[float] = mapped_column(Float, default=0.0)

    neuron: Mapped["Neuron"] = relationship()
    competition: Mapped["Competition"] = relationship()
