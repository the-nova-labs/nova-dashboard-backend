from sqlalchemy import Integer, String, Float, ForeignKey, Table, Column
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
    name: Mapped[str] = mapped_column(String, index=True)


# Association tables for many-to-many relationships
competition_target_association = Table(
    "competition_target_association",
    Base.metadata,
    Column("competition_id", Integer, ForeignKey("competitions.id"), primary_key=True),
    Column("protein_id", Integer, ForeignKey("proteins.id"), primary_key=True),
)


competition_anti_target_association = Table(
    "competition_anti_target_association",
    Base.metadata,
    Column("competition_id", Integer, ForeignKey("competitions.id"), primary_key=True),
    Column("protein_id", Integer, ForeignKey("proteins.id"), primary_key=True),
)

    
class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    epoch_number: Mapped[int] = mapped_column(Integer, nullable=False)
    target_proteins: Mapped[List["Protein"]] = relationship(
        "Protein", 
        secondary=competition_target_association, 
        backref="target_competitions"
    )
    anti_target_proteins: Mapped[List["Protein"]] = relationship(
        "Protein", 
        secondary=competition_anti_target_association, 
        backref="anti_target_competitions"
    )
    submissions: Mapped[List["Submission"]] = relationship(back_populates="competition")
    best_submission: Mapped["Submission"] = relationship(
        "Submission",
        primaryjoin="and_(Competition.id==Submission.competition_id)",
        order_by="desc(Submission.score), asc(Submission.block_number), asc(Submission.id)",
        uselist=False,
        viewonly=True
    )
    

class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    block_number: Mapped[int] = mapped_column(Integer, nullable=False)
    competition_id: Mapped[int] = mapped_column(Integer, ForeignKey("competitions.id"), nullable=False)
    neuron_id: Mapped[int] = mapped_column(Integer, ForeignKey("neurons.id"), nullable=False)
    molecule: Mapped[str] = mapped_column(String, default="")
    score: Mapped[float] = mapped_column(Float, default=0.0)

    neuron: Mapped["Neuron"] = relationship()
    competition: Mapped["Competition"] = relationship()
