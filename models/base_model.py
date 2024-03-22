#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import os
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
# from models import storage
Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        from models import storage
        self.id = str(uuid.uuid4())
        if not kwargs:
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

        else:
            try:
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            except KeyError:
                # kwargs['updated_at'] = datetime.now()
                setattr(self, 'updated_at', datetime.utcnow())
            try:
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            except KeyError:
                setattr(self, 'created_at', datetime.utcnow())
            try:
                del kwargs['__class__']
            except KeyError:
                pass
            # for every key-value pair,
            # instance attribute is created from dictionary
            # Should be tested
            for key, value in kwargs.items():
                setattr(self, key, value)
            # self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        # try:
        #     if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        #         del self.__dict__['_sa_instance_state']
        # except Exception:
            # pass
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def __repr__(self):
        """Returns string representation when str() is used"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        # try:
        #     if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        #         del self.__dict__['_sa_instance_state']
        # except Exception:
        #     pass
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        # print("before update_ta")
        self.updated_at = datetime.now()
        # print("after update_ta")
        storage.new(self)  # moved from def __init__
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        key_to_remove = '_sa_instance_state'
        # print("Dictionary before deletion", dictionary)
        if key_to_remove in dictionary:
            if os.getenv('HBNB_TYPE_STORAGE') != 'db':
                del dictionary[key_to_remove]
            # print("Dictionary after deletion", dictionary)
        return dictionary

    def delete(self):
        """Delets the current instance from storage"""
        from models import storage
        storage.delete(self)
