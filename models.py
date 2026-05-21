from database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship


class TravelProject(Base):

    __tablename__ = "travel_projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    start_date = Column(
        String,
        nullable=True
    )

    places = relationship(
        "ProjectPlace",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    @property
    def completed(self):

        return (
            len(self.places) > 0
            and all(
                place.visited
                for place in self.places
            )
        )


class ProjectPlace(Base):

    __tablename__ = "project_places"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("travel_projects.id")
    )

    external_id = Column(
        Integer,
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    notes = Column(
        Text,
        nullable=True
    )

    visited = Column(
        Boolean,
        default=False
    )

    project = relationship(
        "TravelProject",
        back_populates="places"
    )

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "external_id"
        ),
    )