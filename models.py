from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    favorites = relationship("Club")
    def __repr__(self):
        return '<User %r>' % self.username
    pass

class Club(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    club_name = Column(Text, unique=True, nullable=False)
    tags = relationship("Tag")
    user_id = Column(Integer(), ForeignKey('users.id'))
    pass

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String(80))
    club_id = Column(Integer(), ForeignKey('clubs.id'))
