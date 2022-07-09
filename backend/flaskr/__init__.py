import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10
# THIS CODE IS FROM THE BOOKSHELF EXCERCISE FROM THE CLASS ROOM 
# MOST OF MY CODE IS INSPIRED FROM THE CLASSROOM

def paginate_question(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    questions = [question.format() for question in selection]
    c_questions = questions[start:end]
    
    return c_questions
    

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    
    cors = CORS(app, resources={r"/api/*": {"origin": "*"}})
    """
    
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the DONEs
    """

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE'"
        )
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if len(categories)== 0 :
            abort(404)
            
        categories_formatted = {category.id : category.type for category in categories}
            
        return jsonify({
            'success': True,
            'categories': categories_formatted,

        })
        
    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():

        selection = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        questions = paginate_question(request, selection)

        if len(questions)==0:
            abort(404)
            
        categories_formatted = {category.id : category.type for category in categories}

        for i in categories:
           cc= {i.id: i.type}
        #    print(cc)
        # c_category= json.dumps(categories)
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'current_category': cc, 
            'categories': categories_formatted
        })
  
  
  
   
    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
       try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            # print(question)
            
            if question is None:
                abort(404)
            
            question.delete()
            
            return jsonify({
                'success': True,
                'deleted': question_id
            })
            
            
       except:
           abort(422)

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def post_new_question():
        body = request.get_json()
        
        incoming_question = body.get('question', None)
        incoming_answer = body.get('answer', None)
        incoming_category = body.get('category', None)
        incoming_difficulty = body.get('difficulty', None)
        
        try:
            question = Question(question=incoming_question, answer=incoming_answer, category=incoming_category, difficulty=incoming_difficulty )
            
            question.insert()
            return jsonify({
                'success': True,
                'created_id': question.id
            })
        except:
            abort(422)
    
    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_through_question():
        body = request.get_json()
        search = body.get('searchTerm', None)


        try:
            question = Question.query.filter(Question.question.ilike(f'%{search}%'))
            matched_questions= paginate_question(request, question)
            current_category = {i.id: i.category for i in question}
            print(current_category)
            return jsonify({
                "success": True, 
                "questions": matched_questions,
                'total_questions_matched': len(question.all()),
                'current_category': current_category
            })

        except:
            abort(422)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_with_category_id(category_id):

        # SELECT QUESTION WITH CATEGORY_ID
        selection = Question.query.filter(
            Question.category == category_id).all()
        # print(selection)
        categories = Category.query.filter(Category.id == category_id).all()
        questions = paginate_question(request, selection)

        if len(questions) == 0:
            abort(404)

        categories_formatted = {
            category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'current_category': categories_formatted,
        })
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
   
    @app.route('/quizzes', methods=['POST'])
    def post_quizzes():
        body = request.get_json()
        
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        
        # try:
        question = {}
        # get all questions and choice randomly from the questions
        if quiz_category['id'] == 0:
            question = Question.query.filter(Question.id.notin_(previous_questions)).all()
            randchoice = random.choice(question)
            
            
        else:
            categorzed_questions = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()
            
            randchoice = random.choice(categorzed_questions)
            print(randchoice)
            
            if len(previous_questions) >= 5:
                randchoice is None
                
            

        
              
            
        return jsonify({
            'success': True,
            'question':randchoice.format()
        })
        # except:
        #     abort(422)

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # REQUEST NOT FOUND
    @app.errorhandler(404)
    def not_found(error):
        return(
            jsonify({
                'success': False, 
                'error': 404, 
                'message': 'resource not found'
            }), 404
        )

    # BAD REQUEST
    @app.errorhandler(400)
    def not_found(error):
        return(
            jsonify({
                'success': False, 
                'error': 400, 
                'message': 'bad resource'
            }), 400
        )
    # UNPROCESSABLE ENTTIY
    @app.errorhandler(405)
    def not_found(error):
        return(
            jsonify({
                'success': False, 
                'error': 405, 
                'message': 'method not allowd'
            }), 405
        )
        
    # UNPROCESSABLE ENTTIY
    @app.errorhandler(422)
    def not_found(error):
        return(
            jsonify({
                'success': False, 
                'error': 422, 
                'message': 'unprocessable entity'
            }), 400
        )
        
    # INTERNAL SERVER ERROR
    @app.errorhandler(500)
    def not_found(error):
        return(
            jsonify({
                'success': False, 
                'error': 500, 
                'message': 'intenal server error'
            }), 500
        )

    return app

