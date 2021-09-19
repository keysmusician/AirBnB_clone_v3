#!/usr/bin/python3
"""Holds class State"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    if models.storage_t != "db":
        @property
        def cities(self):
            """Returns a list of City instances linked to this state"""
            all_cities = models.storage.all(City).values()
            return [city for city in all_cities if city.state_id == self.id]
