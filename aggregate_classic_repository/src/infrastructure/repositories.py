from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session

from aggregate_classic_repository.src.domain.forum import QuestionRepository, Votes, Question, Answer
from common import exceptions

Base = declarative_base()


class QuestionRow(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    title = Column(String)
    text = Column(String)
    votes_up = Column(Integer)
    votes_down = Column(Integer)
    answers = relationship("AnswerRow", backref="questions", order_by="AnswerRow.id",
                           cascade="all, delete, delete-orphan")


class AnswerRow(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    question_id = Column(ForeignKey('questions.id'))
    author_id = Column(Integer)
    text = Column(String)


class ORMQuestionRepository(QuestionRepository):

    def __init__(self, session: Session):
        self._session = session
        self._query = self._session.query(QuestionRow)

    def get(self, question_id, for_read) -> Question:
        if for_read:
            query = self._query
        else:
            query = self._query.with_for_update()

        question_row = query.filter_by(id=question_id).one_or_none()
        if not question_row:
            raise exceptions.NotFound(question_id)
        return self.__create_question_from_row(question_row)

    def get_all(self, for_read) -> list:
        return [self.__create_question_from_row(question_row) for question_row in self._query.filter()]

    def add(self, question: Question) -> None:
        self._session.add(self.__create_row_from_question(question))
        self._session.commit()

    def update(self, question: Question) -> None:
        self._session.merge(self.__create_row_from_question(question))
        self._session.commit()

    def remove(self, question: Question) -> None:
        question_row = self._session.merge(self.__create_row_from_question(question))
        self._session.delete(question_row)
        self._session.flush()

    @staticmethod
    def __create_row_from_question(question: Question) -> QuestionRow:
        answer_rows = []

        for answer in question.answers:
            answer_row = AnswerRow()
            answer_row.id = answer.id
            answer_row.author_id = answer.author_id
            answer_row.question_id = question.id
            answer_row.text = answer.text
            answer_rows.append(answer_row)

        question_row = QuestionRow()
        question_row.id = question.id
        question_row.title = question.title
        question_row.text = question.text
        question_row.author_id = question.author_id
        question_row.votes_up = question.votes.up
        question_row.votes_down = question.votes.down
        question_row.answers = answer_rows

        return question_row

    @staticmethod
    def __create_question_from_row(question_row):
        votes = Votes(question_row.votes_up, question_row.votes_down)
        answers = [
            Answer(
                answer_row.id,
                answer_row.text,
                answer_row.author_id
            )
            for answer_row in question_row.answers
        ]
        return Question(
            question_row.id,
            question_row.title,
            question_row.text,
            question_row.author_id,
            votes,
            answers
        )
