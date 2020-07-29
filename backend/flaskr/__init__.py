import sys
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

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

  def paginate_questions(request):
    question = request.args.get('page', 1, type=int)
    questions = Question.query.order_by(
      Question.id.asc()
    ).paginate_questions(question, per_page=QUESTIONS_PER_PAGE).items
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
      return question.format()

  @app.route('/questions')
  def get_questions():
    try:
      return jsonify({
        'success': True,
        'questions': paginate_questions(request),
        'total_questions': Question.count()
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

  @app.route('/question/<int:question_id>', method=['DELETE'])
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
  @app.route('/question', method=['POST'])
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
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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

    