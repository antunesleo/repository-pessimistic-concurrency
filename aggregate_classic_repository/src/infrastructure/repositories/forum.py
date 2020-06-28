from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    title = Column(String)
    text = Column(String)
    votes_up = Column(Integer)
    votes_down = Column(Integer)
    answers = relationship("Answer", backref="questions", order_by="Answer.id",
                           cascade="all, delete, delete-orphan")


class Answer(Base):
    __tablename__ = 'Answers'

    id = Column(Integer, primary_key=True)
    question_id = Column(ForeignKey('questions.id'))
    author_id = Column(Integer)
    text = Column(String)
