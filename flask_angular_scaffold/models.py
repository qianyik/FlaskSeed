import datetime
import json
from flask import jsonify, make_response
from sqlalchemy import (
    Column,
    CHAR,
    Enum,
    func,
    Integer,
    ForeignKey,
    String,
    TIMESTAMP,
    DateTime,
    Text,
    Boolean
)
from flask_angular_scaffold.database import Base

Base = Base


class Base_Model(Base):
    __abstract__ = True

    date_representations = [] #Need for to_dict
    timestamp_representations = [] #Need for api_base -> single_put

    def format_value(self, name):
        value = Base.__getattribute__(self, name)

        if name in self.date_representations and value is not None:
            value = value.isoformat()

        return value

    def to_dict(self):
        return {c.name: self.format_value(c.name) for c in self.__table__.columns}

class Project(Base_Model):
    __tablename__ = 'project'
    __table_args__ = {'mysql_engine':'InnoDB'}

    #Need to override base if model has date, datetimes, or timestamps
    date_representations = ['created','modified'] #Need for to_dict. All representations go here
    timestamp_representations = ['modified'] #Need for api_base -> single_put

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    short_synopsis = Column(String(100))
    long_synopsis = Column(String(1000))
    created = Column(DateTime, default = datetime.datetime.now(), nullable = False)
    modified = Column(TIMESTAMP, nullable = False)
    website = Column(String(100))
    location = Column(String(300))
    organization = Column(String(100), nullable = False)

    # Keeping this to show how foreign keys are done inside models
    #contact = Column(Integer, ForeignKey('contact.id'), nullable = False)


class Contact(Base_Model):
    __tablename__ = 'contact'
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(30))
    email = Column(String(50), nullable = False)
    phone = Column(String(30))
    ufid = Column(String(8))

