import os
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
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "Open", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)
         
        pass

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
    Write at least one test for each test for successful operation and for expected errors.
    """
    # TEST GET CATEGORIES SUCCESS BEHAVIOUR
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['categories'])
       
    # TEST GET CATEGORIES ERROR BEHAVIOUR
    def test_404_categories_with_wrong_route(self):
        res = self.client().get('/categories1')
        data = json.loads(res.data)
        
      
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')
        
   
    # TEST GET QUESTIONS SUCCESS BEHAVIOUR
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])
       
    #TEST  GET CATEGORIES ERROR BEHAVIOUR
    def test_404_questions_beyond_pagination(self):
        res = self.client().get('/questions/?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')
        
   #TEST  GET QUESTIONS FOR EACH CATEGORY SUCCESS BEHAVIOUR
    def test_fetching_question_for_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
       
    #TEST  GET QUESTIONS FOR EACH CATEGORY ERROR BEHAVIOUR
    def test_404_category_over_categories(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')
        
   
    #TEST  DELETE QUESTION SUCCESS BEHAVIOUR
    # I COMMENT IT OUT IN ORDER NOT TO THROUGH ERRORS BECAUSE IT DELEETES THE ID ANYTIME IT RUNS
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/11')
    #     data = json.loads(res.data)
        
    #     question = Question.query.filter(Question.id == 11).one_or_none()
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['deleted'], 11)
    #     self.assertEqual(question, None)
       
    #TEST  DELETE QUESTION ERROR BEHAVIOUR
    def test_422_delete_question_does_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable entity')
        
   
        
   #TEST  POST QUESTION SUCCESS BEHAVIOUR
    def test_posting_new_question(self):
        res = self.client().post('/questions', json={"question": "whats your name"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        pass
    #TEST  POST QUESTION ERROR BEHAVIOUR

    def test_422_posting_new_question_decline(self):
        res = self.client().post(
            '/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        pass
   
   #TEST SEARCH QUESTION SUCCESS BEHAVIOUR
    def test_searching_through_questions(self):
        res = self.client().post(
            '/questions/search', json={"search": "Who discovered penicillin?"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['current_category'], {})
        
    #TEST SEARCH QUESTION ERROR BEHAVIOUR

    def test_searching_through_questions_without_match(self):
        res = self.client().post(
            '/questions/search', json={"search": "programing fantasy"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions_matched'], 0)
        
   
   #TEST GET QUESTIONS TO PLAY THE QUIZ SUCCESS BEHAVIOUR
    def test_get_questions_for_quiz(self):
        res = self.client().post(
            '/quizzes', json={
                'previous_questions': [1, 4, 20, 15],
                'quiz_category': 'current category'
            })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'])
        
    #TEST GET QUESTIONS TO PLAY THE QUIZ ERROR BEHAVIOUR

    def test_searching_through_questions_without_match(self):
        res = self.client().post(
            '/quizzes', )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['total_questions_matched'], 0)
        
   
   


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()