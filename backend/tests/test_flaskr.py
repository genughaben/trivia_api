import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgresql://company_data:rightpassword@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each endpoint for successful operation and for expected errors.
    """

    def test_categories(self):
        """
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_categories
        """

        response = self.client.get('/categories')
        result: json = response.get_json()

        self.assertTrue('categories' in result)
        self.assertEqual(len(result['categories']), 6)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertEqual(response.status_code, 200)

    def test_list_questions(self):
        """
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_list_questions
        """

        response = self.client.get('/questions')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertTrue('questions' in result)
        self.assertEqual(len(result['questions']), 10)
        self.assertTrue('total_questions' in result)
        self.assertEqual(result['total_questions'], 19)
        self.assertTrue('categories' in result)
        self.assertEqual(len(result['categories']), 6)


    def test_delete_questions(self):
        """
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_list_questions
        """

        question = Question(
            question="Example question?",
            answer="Example answer",
            difficulty=3,
            category=Category.query.filter_by(type="Sports").first()
        )

        question.insert()
        question_id = question.id

        self.assertEqual(Question.count(), 20)

        response = self.client.delete(f'/questions/{question_id}')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertTrue('deleted' in result)
        self.assertEqual(result['deleted'], question_id)
        self.assertTrue('questions' in result)
        self.assertEqual(len(result['questions']), 10)
        self.assertTrue('total_questions' in result)
        self.assertEqual(result['total_questions'], 19)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
