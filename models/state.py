#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            'City', cascade='all, delete-orphan', backref='state')
    else:
        @property
        def cities(self):
            """
            Getter attribute that returns a list of City instances
            with state_id equals to the provided state_id.
            """
            from models import storage
            from models.city import City

            cities_list = []
            for city_instance in storage.all(City).values():
                if city_instance.state_id == self.id:
                    cities_list.append(city_instance)
            return cities_list
