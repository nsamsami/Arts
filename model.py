import config
import bcrypt
from datetime import datetime
import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

# These are imported for uploading files
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

engine = create_engine(config.DB_URI, echo=False)
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))


Base = declarative_base()
Base.query = session.query_property()
sqlite_autoincrement=True


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)
 
    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)
    title = Column(String(64), nullable=True)
    name = Column(String(64), nullable=False)
    image_1 = Column(String(64), nullable=True)
    image_2 = Column(String(64), nullable=True)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password


# This creates the tables. drop_all is a hack to delete tables and recreate them. Needs a more permanent solution. 
def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def seed():
    Base.metadata.create_all(engine)
    u = User(email="nahid@gmail.com", title="Art Photo", name="Nahid Samsami")
    u.set_password("pass")
    session.add(u)
    session.commit()
    print "Tables completed"

if __name__ == "__main__":
    create_tables()
    seed()
    print "Created tables"
