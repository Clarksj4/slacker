import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Author: Matt Ankerson
# Date: 27 March 2015

Base = declarative_base()

# tables

# we need to store email, password and screen name.

class User(Base):
    __tablename__ = 'user'
    # define columns
    id = Column(String(200), nullable=False, primary_key=True)
    password = Column(String(200), nullable=False)
    screen_name = Column(String(200), nullable=False)
    
# Create an engine that stores data in the local directory's
# sqlalchemy_users.db file.
engine = create_engine('sqlite:///sqlalchemy_users.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
        


