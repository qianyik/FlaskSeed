import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import get_config

config = get_config()

engine = (
    create_engine(
        config.get('Database', 'SQLALCHEMY_DATABASE_URI'),
        convert_unicode=True, pool_recycle=3600)
    )

Session = (
    scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
    )
)

Base = declarative_base()
Base.query = Session.query_property()
Base.metadata.bind = engine


def init_db():
    from flask_angular_scaffold.models import Base
    print "Adding DB tables"
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
