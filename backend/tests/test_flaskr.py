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

    def test_incoming_payload_not_json(self):
        """
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_categories
        """

        not_json_input = False

        response = self.client.post(path='/questions',
                                    json=not_json_input,
                                    content_type='application/json')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertTrue('success' in result)
        self.assertEqual(result['success'], False)
        self.assertTrue(result['message'].startswith('Bad request: '))

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

        response = self.client.get('/questions?page=2')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertTrue('questions' in result)
        self.assertEqual(len(result['questions']), 9)
        self.assertTrue('total_questions' in result)
        self.assertEqual(result['total_questions'], 19)
        self.assertTrue('categories' in result)
        self.assertEqual(len(result['categories']), 6)

    def test_return_404_for_page_count_too_high(self):
        """
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_return_404_for_page_count_too_high
        """

        response = self.client.get('/questions?page=4')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertTrue('success' in result)
        self.assertEqual(result['success'], False)
        self.assertTrue(result['message'].startswith('Not found: '))


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

    def test_create_questions(self):
        """
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_create_questions
        """

        questions_count_before_insert = Question.count()

        request_json = {
            "question": "Example question?",
            "answer": "Example answer",
            "difficulty": 3,
            "category": Category.query.filter_by(type="Sports").first().id
        }

        response = self.client.post(path='questions',
                                    json=request_json,
                                    content_type='application/json')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])

        EXPECTED_QUESTION_RESULT = {
            "question": "Example question?",
            "answer": "Example answer",
            "difficulty": 3,
            "category": 6
        }

        self.assertTrue('question' in result)
        self.assertEqual(result['question']['question'], EXPECTED_QUESTION_RESULT['question'])
        self.assertEqual(result['question']['answer'], EXPECTED_QUESTION_RESULT['answer'])
        self.assertEqual(result['question']['difficulty'], EXPECTED_QUESTION_RESULT['difficulty'])
        self.assertEqual(result['question']['category'], EXPECTED_QUESTION_RESULT['category'])

        question_count_after_insert = Question.count()
        self.assertEqual(questions_count_before_insert + 1, question_count_after_insert)

        # clean up
        questions_to_clean = Question.query.filter_by(question=request_json['question'],
                                                      answer=request_json['answer']).all()
        for q in questions_to_clean:
            q.delete()


    def test_search_questions(self):
        """
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_search_questions
        """

        request_json = {
            "searchTerm": "Soccer"
        }

        response = self.client.post(path='questions/search',
                                    json=request_json,
                                    content_type='application/json')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertTrue('questions' in result)
        self.assertEqual(len(result['questions']), 2)
        self.assertTrue('total_questions' in result)
        self.assertEqual(result['total_questions'], 19)


    def test_get_questions_by_category_id(self):
        """
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_get_questions_by_category_id
        """

        category_id = 6 # id for category 'Sports'

        response = self.client.get(path=f'categories/{category_id}/questions')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertTrue('questions' in result)
        self.assertEqual(len(result['questions']), 2)
        self.assertTrue('total_questions' in result)
        self.assertEqual(result['total_questions'], 19)


    def test_play(self):
        """
        Cases:
        * first question from any category
        * second question from any category
        * another question from category with not enough questions for a whole game is loaded, hence it is drawn from all
        Inspection
        ----------
        > python -m unittest test_flaskr.TriviaTestCase.test_play
        """

        # CASE #1 first question from any category (here: Sports)

        category_type = "Sports"
        category_id = 6 # category_id for category 'Sports'

        request_json = {
            "previous_questions": [],
            "quiz_category": {"type": f"{category_type}", "id": f"{category_id}"},
        }

        response = self.client.post(path='play',
                                    json=request_json,
                                    content_type='application/json')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertTrue('question' in result)
        self.assertEqual(result['question']['category'], int(category_id))

        # CASE #2 second question from any category

        request_json = {
            "previous_questions": [10],
            "quiz_category": {"type": f"{category_type}", "id": f"{category_id}"},
        }

        response = self.client.post(path='play',
                                    json=request_json,
                                    content_type='application/json')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertTrue('question' in result)
        self.assertEqual(result['question']['category'], int(category_id))

        # CASE #3 first question from any category (here: Sports)

        request_json = {
            "previous_questions": [10, 11],
            "quiz_category": {"type": f"{category_type}", "id": f"{category_id}"},
        }

        response = self.client.post(path='play',
                                    json=request_json,
                                    content_type='application/json')
        result: json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertTrue('question' in result)
        self.assertNotEqual(result['question']['category'], int(category_id))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
