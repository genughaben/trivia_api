import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db


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

        # EXPECTED RESULT:

        response = self.client.get('categories')
        result: json = response.get_json()

        self.assertTrue('categories' in result)
        self.assertEqual(len(result['categories']), 6)
        self.assertTrue('success' in result)
        self.assertTrue(result['success'])
        self.assertEqual(response.status_code, 200)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
