from abc import ABC, abstractmethod

from common import exceptions
from common.domain import Aggregate, Entity, ValueObject


class Answer(Entity):

    @property
    def id(self):
        return self.__id

    @property
    def text(self):
        return self.__text

    @property
    def author_id(self):
        return self.__author_id

    def __init__(self, id, text, author_id):
        self.__id = id
        self.__text = text
        self.__author_id = author_id

    def change_text(self, text: str):
        self.__text = text


class Votes(ValueObject):

    @property
    def up(self):
        return self.__up

    @property
    def down(self):
        return self.__down

    def __init__(self, up, down):
        self.__up = up
        self.__down = down


class Question(Aggregate):

    def __init__(self, id: int, title: str, text: str, author_id: int, votes: Votes, answers: list):
        self.__id = id
        self.__title = title
        self.__text = text
        self.__author_id = author_id
        self.__votes = votes
        self.__answers = answers

    @property
    def id(self):
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def text(self) -> str:
        return self.__title

    @property
    def author_id(self) -> int:
        return self.__author_id

    @property
    def votes(self) -> Votes:
        return self.__votes

    @property
    def answers(self) ->  list:
        return self.__answers

    def to_answer(self, answer: Answer):
        self.__answers.append(answer)

    def remove_answer(self, answer_id):
        answer_to_remove = None
        for answer in self.__answers:
            if answer.id == answer_id:
                answer_to_remove = answer

        try:
            self.__answers.remove(answer_to_remove)
        except ValueError:
            raise exceptions.NotFound('answer_id {} not found in question'.format(answer_id))

    def edit_title(self, title: str):
        self.__title = title

    def vote_up(self):
        self.__votes = Votes(self.__votes.up+1, self.__votes.down)

    def vote_down(self):
        self.__votes = Votes(self.__votes.up, self.__votes.down+1)

    def change_answer_text(self, answer_id, new_text):
        for answer in self.__answers:
            if answer.id == answer_id:
                answer.change_text(new_text)
        raise exceptions.NotFound('Answer {} not found'.format(answer_id))


class QuestionRepository(ABC):

    @abstractmethod
    def get(self, id) -> Question:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def add(self, question: Question) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, question: Question) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self, question: Question) -> None:
        raise NotImplementedError
