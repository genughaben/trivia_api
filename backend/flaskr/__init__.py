import sys
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random
from flaskr.validation import *
from flaskr.logger import logger
import traceback

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app)  # , resources={r"/api/*": {"origins": "*"}}

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        error = False
        try:
            categories = Category.query.all()
            category_types = []
            if categories is not None:
                for category in categories:
                    category_types.append(category.type)
        except:
            error = True
            print(sys.exc_info())

        if error:
            abort(404)
        return jsonify(category_types)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    def paginate_questions(page):
        return Question.query.order_by(
            Question.id.asc()
        ).paginate(page, per_page=QUESTIONS_PER_PAGE).items

    def paginate_filter_questions(page, field, like_term):
        return Question.query.order_by(
            Question.id.asc()
        ).filter(getattr(Question, field).ilike(f"%{str(like_term).lower()}%") if field != 'category_id' else True
        ).filter(getattr(Question, field) == like_term if field == 'category_id' else True
        ).paginate(page, per_page=QUESTIONS_PER_PAGE).items

    def get_paginate_questions(request, field=None, like_term=None):
        page = request.args.get('page', 1, type=int)
        if field is not None and like_term is not None:
            questions = paginate_filter_questions(page, field, like_term)
        else:
            questions = paginate_questions(page)
        if len(questions) > 0:
            formatted_questions = [q.format() for q in questions]
            return formatted_questions
        else:
            return []

    def paginate_category_questions(request, category):
        page = request.args.get('page', 1, type=int)
        category_questions = Question.query.order_by(
            Question.id.asc()
        ).filter(Question.category.has(type=category)
        ).paginate(page, per_page=QUESTIONS_PER_PAGE).items
        if len(category_questions) > 0:
            formatted_questions = [q.format() for q in category_questions]
            return formatted_questions
        else:
            return []

    def question_or_abort(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        else:
            return question

    @app.route('/questions')
    def get_questions():
        try:
            return jsonify({
                'questions': get_paginate_questions(request),
                'total_questions': Question.count(),
                'categories': { category.id: category.type for category in  Category.query.all() }
            })
        except:
            print(sys.exc_info())
            abort(404)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/question/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = question_or_abort(question_id)
            if question is None:
                abort(404)
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': get_paginate_questions(request),
                'total_questions': Question.count()
            })
        except:
            abort(404)
        finally:
            Question.db_close()

    @app.route('/question/<int:question_id>', methods=['GET'])
    def get_single_questions(question_id):
        try:
            question = question_or_abort(question_id)
            if question is None:
                abort(404)

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(404)
        finally:
            Question.db_close()

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/question', methods=['POST'])
    def create_questions():

        try:
            if request.is_json:
                data = request.get_json()
            else:
                raise ValueError("Error: incorrect MIME-Type")
        except Exception as e:
            abort(400, description="Error: payload is not json")

        try:
            assert valid_string(data, "question"), INVALID_STRING_VALUE_MESSAGE % 'question'
            assert valid_string(data, "answer"), INVALID_STRING_VALUE_MESSAGE % 'answer'
            assert valid_string(data, "category"), INVALID_STRING_VALUE_MESSAGE % 'category'
            assert valid_int(data, "difficulty"), INVALID_INTEGER_VALUE_MESSAGE % 'difficulty'

        except AssertionError as assert_error:
            logger.error(f'{request.path}: 442 {assert_error}')
            abort(422, description=str(assert_error))

        category = Category.query.filter_by(type=data['category']).first()

        question = Question(
            question=data['question'],
            answer=data['answer'],
            difficulty=data['difficulty'],
            category=category
        )

        try:
            question.insert()
            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(404, description=f"{sys.exc_info()} and trace: {traceback.format_exc()}")
            logger.error(f'{request.path}: 404 with {sys.exc_info()} and trace: {traceback.format_exc()}')
        finally:
            Question.db_close()

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/question/search')
    def search_questions():
        try:
            search_term = request.args.get('q')
            print(search_term)
        except Exception as e:
            logger.error(f'TypeError: {e} at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')

        try:
            assert type(search_term) is str, "Search term is not a valid string"
            assert len(search_term)>3, "Search term too short, type at least 3 characters"

        except AssertionError as assert_error:
            logger.error(f'{assert_error}: 422 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(422, description=str(assert_error))

        try:
            return jsonify({
                'success': True,
                'questions': get_paginate_questions(request, 'question', search_term),
                'total_questions': Question.count()
            })
        except Exception as e:
            logger.error(
                f'{e}: 404 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404)
        finally:
            Question.db_close()

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<string:category>/questions')
    def get_questions_for_category_type(category):

        try:
            assert not category.isnumeric(), "Category should not be numeric"

        except AssertionError as assert_error:
            logger.error(f'{assert_error}: 422 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(422, description=str(assert_error))

        try:

            return jsonify({
                'success': True,
                'questions': paginate_category_questions(request, category),
                'total_questions': Question.query.filter(Question.category.has(type=category)).count()
            })
        except Exception as e:
            logger.error(
                f'{e}: 404 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404)
        finally:
            Question.db_close()

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_for_category_id(category_id):

        try:
            assert type(category_id) is int, "Category_id should be numeric"

        except AssertionError as assert_error:
            logger.error(
                f'{assert_error}: 422 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(422, description=str(assert_error))

        try:
            return jsonify({
                'success': True,
                'questions': get_paginate_questions(request, 'category_id', category_id),
                'total_questions': Question.query.filter(category_id==category_id).count()
            })
        except Exception as e:
            logger.error(
                f'{e}: 404 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404)
        finally:
            Question.db_close()

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/play', methods=['POST'])
    def play_trivia():

        try:
            if request.is_json:
                data = request.get_json()
            else:
                raise ValueError("Error: incorrect MIME-Type")
        except Exception as e:
            abort(400, description=f"Error {e}: payload is not json")

        try:
            if 'question_ids' in data:
                assert valid_numbers_array(data, "question_ids"), INVALID_NUMBERS_ARRAY_MESSAGE_TEMPLATE % 'question_ids'
            if 'category' in data:
                assert valid_string(data, "category"), INVALID_STRING_VALUE_MESSAGE % 'category'

        except AssertionError as assert_error:
            logger.error(f'{request.path}: 442 {assert_error}')
            abort(422, description=str(assert_error))

        category = data['category'] if 'category' in data else None
        question_ids = data['question_ids'] if 'question_ids' in data else None

        q = Question.query\
            .filter( Question.category.has(type=category) if category else True)\
            .filter(~Question.id.in_(question_ids) if question_ids else True).order_by(
                func.random()
            ).first()

        try:
            return jsonify({
                'success': True,
                'question': q.format() if q is not None else f"all questions of {data['category']} answered"
            })
        except:
            abort(404, description=f"{sys.exc_info()} and trace: {traceback.format_exc()}")
            logger.error(f'{request.path}: 404 with {sys.exc_info()} and trace: {traceback.format_exc()}')
        finally:
            Question.db_close()

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "data": [],
            "error": 404,
            "message": f"Not found: {error}"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "data": [],
            "error": 422,
            "message": f"Unprocessable: {error}"
        }), 422

    return app
