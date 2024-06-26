from sqlalchemy import Column, Date, ForeignKey, Integer

from src import db


class ObservationPeriod(db.Model):
    __tablename__ = "observation_period"

    observation_period_id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("person.person_id"), nullable=False)
    observation_period_start_date = Column(Date, nullable=False)
    observation_period_end_date = Column(Date, nullable=False)
    period_type_concept_id = Column(Integer, nullable=False)
