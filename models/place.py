#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from models.user import User
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey(City.id), nullable=False)
    user_id = Column(String(60), ForeignKey(User.id), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship('Review', cascade='all, delete-orphan',
                           backref='place')
    amenities = relationship('Amenity', secondary='place_amenity',
                             viewonly=False)
    place_amenity = Table(
        'place_amenity', Base.metadata,
        Column('place_id', ForeignKey('places.id')),
        Column('amenity_id', ForeignKey('amenities.id'))
    )   

    @property
    def reviews(self, place_id):
        """getter attribute reviews that returns the list of Review
        instances with place_id equals to the current Place.id"""
        from models import storage

        reviews_list = []
        for place_instance in storage.all():
            if place_instance.place_id == self.id:
                reviews_list.append(place_instance)
        return reviews_list

    @property
    def amenities (self, amenity_ids):
        """Getter attribute amenities that returns the list of Amenity
        instances based on the attribute amenity_ids that contains all
        Amenity.id linked to the Place"""
        
        return self.amenity_ids

    @setattr
    def amenities(self, amenity_obj):
        """Setter attribute"""
        from models.amenity import Amenity

        if isinstance(amenity_obj, Amenity):
            self.amenity_ids.append(amenity_obj.id)