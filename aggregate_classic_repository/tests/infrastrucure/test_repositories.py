import os
import unittest
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aggregate_classic_repository.src.domain.forum import Answer, Votes, Question
from aggregate_classic_repository.src.infrastructure.repositories import ORMQuestionRepository
from common import exceptions


class TestORMQuestionRepository(unittest.TestCase):

    def setUp(self) -> None:
        # os.system("cd /home/antunesleo/projects/parallel-aggregates/aggregate_classic_repository && touch aggregate-classic-repository.db && alembic upgrade head")
        some_engine = create_engine('postgresql+pg8000://aggregate_classic_repository:aggregate_classic_repository@localhost/aggregate_classic_repository')
        SessionMaker = sessionmaker(bind=some_engine)
        self.__session = SessionMaker()
        self.__orm_question_repository = ORMQuestionRepository(self.__session)

    def test_should_add_new_question(self):
        question = Question(
            None,
            'sed varius lectus accumsan',
            '''Morbi feugiat felis sollicitudin ipsum tincidunt, at congue lectus maximus. 
               Donec vehicula venenatis scelerisque. Proin nec purus vel diam 
               blandit cursus at ac dolor. 
               Fusce vel metus tellus. Nullam sed ligula ut lacus feugiat cursus. 
               Etiam pellentesque purus in purus ornare dapibus. 
               Donec gravida mauris eu venenatis fermentum.''',
            3,
            Votes(5, 9),
            [
                Answer(None, 'Cras molestie dui vitae nisl tempus', 1),
                Answer(None, 'Vestibulum eu sapien vitae justo aliquet rhoncus non sed mauris', 2),
                Answer(None, 'Vivamus tincidunt semper risus eget euismod.', 3)
            ]
        )
        self.__orm_question_repository.add(question)

        questions = self.__orm_question_repository.get_all(for_read=True)
        self.assertEqual(len(questions), 1)
        self.assertIsInstance(questions[0], Question)
        self.assertEqual(questions[0].title, 'sed varius lectus accumsan')
        self.assertEqual(len(questions[0].answers), 3)
        self.assertIsInstance(questions[0].answers[0], Answer)
        self.assertEqual(questions[0].answers[0].text, 'Cras molestie dui vitae nisl tempus')

    def test_should_answer_question(self):
        question = Question(
            None,
            'sed varius lectus accumsan',
            '''Morbi feugiat felis sollicitudin ipsum tincidunt, at congue lectus maximus. 
               Donec vehicula venenatis scelerisque. Proin nec purus vel diam 
               blandit cursus at ac dolor. 
               Fusce vel metus tellus. Nullam sed ligula ut lacus feugiat cursus. 
               Etiam pellentesque purus in purus ornare dapibus. 
               Donec gravida mauris eu venenatis fermentum.''',
            3,
            Votes(5, 9),
            [
                Answer(None, 'Cras molestie dui vitae nisl tempus', 1),
                Answer(None, 'Vestibulum eu sapien vitae justo aliquet rhoncus non sed mauris', 2),
                Answer(None, 'Vivamus tincidunt semper risus eget euismod.', 3)
            ]
        )
        self.__orm_question_repository.add(question)
        question = self.__orm_question_repository.get(1, for_read=True)
        question.to_answer(Answer(None, 'Curabitur eu sem sit amet ipsum fermentum ullamcorper ut at diam.', 5))
        self.__orm_question_repository.update(question)
        question = self.__orm_question_repository.get(1,  for_read=True)
        self.assertIsInstance(question, Question)
        self.assertEqual(question.title, 'sed varius lectus accumsan')
        self.assertEqual(len(question.answers), 4)
        self.assertIsInstance(question.answers[0], Answer)
        self.assertEqual(question.answers[0].text, 'Cras molestie dui vitae nisl tempus')

    def test_should_update_question(self):
        question = Question(
            None,
            'sed varius lectus accumsan',
            '''Morbi feugiat felis sollicitudin ipsum tincidunt, at congue lectus maximus. 
               Donec vehicula venenatis scelerisque. Proin nec purus vel diam 
               blandit cursus at ac dolor. 
               Fusce vel metus tellus. Nullam sed ligula ut lacus feugiat cursus. 
               Etiam pellentesque purus in purus ornare dapibus. 
               Donec gravida mauris eu venenatis fermentum.''',
            3,
            Votes(5, 9),
            []
        )
        self.__orm_question_repository.add(question)
        # morreu
        question = self.__orm_question_repository.get(3, for_read=False)
        question.edit_title('AAAAAAAA')
        self.__orm_question_repository.update(question)
        question = self.__orm_question_repository.get(3, for_read=False)
        self.assertIsInstance(question, Question)
        self.assertEqual(question.title, 'AAAAAAAA')

    def test_should_remove_answer(self):
        question = Question(
            None,
            'sed varius lectus accumsan',
            '''Morbi feugiat felis sollicitudin ipsum tincidunt, at congue lectus maximus. 
               Donec vehicula venenatis scelerisque. Proin nec purus vel diam 
               blandit cursus at ac dolor. 
               Fusce vel metus tellus. Nullam sed ligula ut lacus feugiat cursus. 
               Etiam pellentesque purus in purus ornare dapibus. 
               Donec gravida mauris eu venenatis fermentum.''',
            3,
            Votes(5, 9),
            [
                Answer(None, 'Cras molestie dui vitae nisl tempus', 1),
                Answer(None, 'Vestibulum eu sapien vitae justo aliquet rhoncus non sed mauris', 2),
                Answer(None, 'Vivamus tincidunt semper risus eget euismod.', 3)
            ]
        )
        self.__orm_question_repository.add(question)

        question = self.__orm_question_repository.get(1)
        question.remove_answer(1)
        self.__orm_question_repository.update(question)
        question = self.__orm_question_repository.get(1)
        self.assertIsInstance(question, Question)
        self.assertEqual(len(question.answers), 2)

    def test_should_remove(self):
        question = Question(
            None,
            'sed varius lectus accumsan',
            '''Morbi feugiat felis sollicitudin ipsum tincidunt, at congue lectus maximus. 
               Donec vehicula venenatis scelerisque. Proin nec purus vel diam 
               blandit cursus at ac dolor. 
               Fusce vel metus tellus. Nullam sed ligula ut lacus feugiat cursus. 
               Etiam pellentesque purus in purus ornare dapibus. 
               Donec gravida mauris eu venenatis fermentum.''',
            3,
            Votes(5, 9),
            []
        )
        self.__orm_question_repository.add(question)
        question = self.__orm_question_repository.get(1)
        self.__orm_question_repository.remove(question)
        with self.assertRaises(exceptions.NotFound):
            self.__orm_question_repository.get(1)

    def test_not_should_overload(self):
        # question = Question(
        #     None,
        #     'sed varius lectus accumsan',
        #     '''Morbi feugiat felis sollicitudin ipsum tincidunt, at congue lectus maximus.
        #        Donec vehicula venenatis scelerisque. Proin nec purus vel diam
        #        blandit cursus at ac dolor.
        #        Fusce vel metus tellus. Nullam sed ligula ut lacus feugiat cursus.
        #        Etiam pellentesque purus in purus ornare dapibus.
        #        Donec gravida mauris eu venenatis fermentum.''',
        #     3,
        #     Votes(5, 9),
        #     []
        # )
        # self.__orm_question_repository.add(question)

        # simulando a pika
        question = self.__orm_question_repository.get(1)
        sleep(10)
        # question.to_answer(Answer(None, 'aaaaaaa', 2))
        question.edit_title(question.title + 'A')
        self.__orm_question_repository.update(question)

    def test_not_should_overload_answer(self):
        # question = Question(
        #     None,
        #     'sed varius lectus accumsan',
        #     '''Morbi feugiat felis sollicitudin ipsum tincidunt, at congue lectus maximus.
        #        Donec vehicula venenatis scelerisque. Proin nec purus vel diam
        #        blandit cursus at ac dolor.
        #        Fusce vel metus tellus. Nullam sed ligula ut lacus feugiat cursus.
        #        Etiam pellentesque purus in purus ornare dapibus.
        #        Donec gravida mauris eu venenatis fermentum.''',
        #     3,
        #     Votes(5, 9),
        #     []
        # )
        # self.__orm_question_repository.add(question)

        # simulando a pika
        question = self.__orm_question_repository.get(1)
        sleep(10)
        question.to_answer(Answer(None, 'aaaaaaa', 2))
        self.__orm_question_repository.update(question)

    def test_should_get_and_update(self):
        question = self.__orm_question_repository.get(1, for_read=False)
        sleep(5)
        question.edit_title(question.title + 'A')
        self.__orm_question_repository.update(question)

    def test_should_get_and_forget_for_a_long_time(self):
        question = self.__orm_question_repository.get(1, for_read=True)
        sleep(30)

    def tearDown(self) -> None:
        # os.system("cd /home/antunesleo/projects/parallel-aggregates/aggregate_classic_repository && rm aggregate-classic-repository.db")
        pass
