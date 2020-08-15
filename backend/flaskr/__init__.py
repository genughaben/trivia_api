import sys
import traceback

from flask import Flask
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func

from flaskr.logger import logger
from flaskr.validation import *
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

'''
******
*** NB: For each endpoint, usage examples can be found in the postman collection 'trivia.postman_collection.json'
******
'''



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
        try:
            categories = Category.query.all()
            category_types = {}
            if categories is not None:
                for category in categories:
                    category_types[category.id] = category.type
        except:
            logger.error(f'{request.path}: 404 with {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404)

        return jsonify({
            'success': True,
            'categories': category_types
        })

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

    def paginate_questions(request, filter_func=lambda: True):
        page = request.args.get('page', 1, type=int)
        questions = Question.query.order_by(
            Question.id.asc()
        ).filter(filter_func()).paginate(page, per_page=QUESTIONS_PER_PAGE).items
        if len(questions) > 0:
            formatted_questions = [q.format() for q in questions]
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
                'success': True,
                'questions': paginate_questions(request),
                'total_questions': Question.count(),
                'categories': {category.id: category.type for category in Category.query.all()}
            })
        except:
            logger.error(f'{request.path}: 404 with {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = question_or_abort(question_id)
            if question is None:
                abort(404)
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': paginate_questions(request),
                'total_questions': Question.count()
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

    @app.route('/questions', methods=['POST'])
    def create_questions():
        try:
            data: json = extract_incoming_json(request)
        except Exception as e:
            abort(400, description=f'Bad request with {e}')

        try:
            assert valid_string(data, "question"), INVALID_STRING_VALUE_MESSAGE % 'question'
            assert valid_string(data, "answer"), INVALID_STRING_VALUE_MESSAGE % 'answer'
            assert valid_int(data, "category"), INVALID_STRING_VALUE_MESSAGE % 'category'
            assert valid_int(data, "difficulty"), INVALID_INTEGER_VALUE_MESSAGE % 'difficulty'

        except AssertionError as assert_error:
            logger.error(f'{request.path}: 442 {assert_error}')
            abort(422, description=str(assert_error))

        category = Category.query.filter_by(id=data['category']).first()

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
        except IntegrityError:
            logger.error(f'{request.path}: 404 with {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404,
                  description=f"IntegrityError, question was already inserted {sys.exc_info()} and trace: {traceback.format_exc()}")
        except:
            logger.error(f'{request.path}: 404 with {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404, description=f"{sys.exc_info()} and trace: {traceback.format_exc()}")
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

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            data: json = extract_incoming_json(request)
        except Exception as e:
            abort(400, description=f'Bad request with {e}')

        try:
            assert valid_string(data, "searchTerm"), INVALID_STRING_VALUE_MESSAGE % 'searchTerm'
            search_term = data.get('searchTerm', '')
            assert len(search_term) > 3, "Search term too short, type at least 3 characters"

        except AssertionError as assert_error:
            logger.error(
                f'{assert_error}: 422 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(422, description=str(assert_error))

        def filter_question():
            return getattr(Question, 'question').ilike(f"%{str(search_term).lower()}%")

        try:
            return jsonify({
                'success': True,
                'questions': paginate_questions(request, filter_func=filter_question),
                'total_questions': Question.count()
            })
        except Exception as e:
            logger.error(
                f'{e}: 404 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404)
        finally:
            Question.db_close()


    @app.route('/categories/<int:category_id>/questions')
    def get_questions_for_category_id(category_id):
        '''
        GET endpoint to get questions based on category.
        '''

        try:
            assert type(category_id) is int, "Category_id should be numeric"

        except AssertionError as assert_error:
            logger.error(
                f'{assert_error}: 422 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(422, description=str(assert_error))

        def filter_question():
            return Question.category.has(id=category_id)

        try:
            return jsonify({
                'success': True,
                'questions': paginate_questions(request, filter_func=filter_question),
                'total_questions': Question.query.filter(category_id == category_id).count()
            })
        except Exception as e:
            logger.error(
                f'{e}: 404 at {request.path} with: {sys.exc_info()} and trace: {traceback.format_exc()}')
            abort(404)
        finally:
            Question.db_close()


    @app.route('/play', methods=['POST'])
    def play_trivia():
        '''
        POST Endpoint to get questions to play the quiz.

        This endpoint takes a category and previous question parameters
        and returns a random question within the given category,
        if provided, and that is not one of the previous questions.

        If there are not enough questions in a given category, all questions are asked,
        and the the remaining questions are drawn from category 'ALL'
        '''
        try:
            data: json = extract_incoming_json(request)
        except Exception as e:
            abort(400, description=f'Bad request with {e}')

        try:
            if 'previous_questions' in data:
                assert data['previous_questions'] == [] or valid_numbers_array(data,
                                                                               "previous_questions"), INVALID_NUMBERS_ARRAY_MESSAGE_TEMPLATE % 'previous_questions'
            if 'quiz_category' in data:
                assert valid_string(data['quiz_category'], "type"), INVALID_STRING_VALUE_MESSAGE % 'quiz_category_type'
                assert valid_string(data['quiz_category'],
                                    "id"), INVALID_STRING_VALUE_MESSAGE % 'quiz_category_id'

        except AssertionError as assert_error:
            logger.error(f'{request.path}: 442 {assert_error}')
            abort(422, description=str(assert_error))

        category = data['quiz_category'] if 'quiz_category' in data else None
        previous_question_ids = data['previous_questions'] if 'previous_questions' in data else None

        q = Question.query \
            .filter(Question.category.has(type=category['type']) if category else True) \
            .filter(~Question.id.in_(previous_question_ids) if previous_question_ids else True).order_by(
            func.random()
        ).first()

        # in case no question of ask category are left, fill questions with other categories
        if q is None or q.count() == 0:
            q = Question.query \
                .filter(~Question.id.in_(previous_question_ids) if previous_question_ids else True).order_by(
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

    @app.errorhandler(500)
    def server_errror(error):
        return jsonify({
            "success": False,
            "data": [],
            "error": 500,
            "message": f"Server Error: Trivia API failed with: {error}"
        }), 500

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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "data": [],
            "error": 400,
            "message": f"Bad request: {error}"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "data": [],
            "error": 405,
            "message": f"Not allowed: {error}"
        }), 405

    return app
