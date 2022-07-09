# The Trivia Application 

The App Trivia is a game that presents you with questions from six(6) categories which include the science, art, history, entertainment, geography and sports. The application has three sections; the list, the add and play section while the categories is on the left side of the home page along with the list section. The list section randomly list all the questions from all the categories available while the user can select a specific category to get questions from that only. The add section gives the user opportunity to add his question and finally the play section......The user can also search through the questions.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 


## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python 3.7 or above, pip or pip3 for mac and node installed on their local machines for the frontend.

#### Backend'

-Install Virtual Environment

-start the Virtual Environment
```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```

-From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

or 

FLASK_APP=flaskr FLASK_DEBUG=True flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made


The application is to run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

## Create and Populate the database 
Create database with the file trivia.psql and populate the database it.

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
Create test database
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
<path> > trivia.psql
python test_flaskr.py
```
dropdb trivia_test delete the existing test database while creating new one with createdb, pythong test_flaskr.py runs the app for the test. The path insert sql relation to the test database

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/` or `http://localhost:5000/`, which is set as a proxy in the frontend configuration. 


### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail and one when there is problem with the server:
- 400: Bad Request
- 422: Not Processable 
- 404: Resource Not Found
- 405: Method Not Allowed
- 500: Internal Server Error

### Endpoints 
#### GET /questions
- General:
    - Returns a list of question objects, success value, and total number of questions
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` 
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": {
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 17
}
```
#### GET /questions base on category
- General:
    - Returns a current_category, list of questions, success value, and total number of questions in the category
- Sample: `curl http://127.0.0.1:5000/categories/<int:category_id>/questions`

``` 
{
  "current_category": {
    "3": "Geography"
  },
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, and success value.
- `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question": "what is http","answer": "hyperTextTransferProtocol","difficulty": 1, "category": 6}'`
```
{
  "created_id": 43,
  "success": true
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, and success value.
- `curl -X DELETE http://127.0.0.1:5000/questions/16?page=2`
```
{
  "deleted": 43,
  "success": true
}
```
#### POST /questions/search
- General:
    - Sends a post request in order to search for a specific question by search term 
- `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d {"searchTerm": "who"} `
```
{
  "current_category": {
    "5": 4,
    "21": 1
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions_matched": 2
}
```
#### POST /questions/quizzes
- General:
    - Sends a post request in order to get the next question to play a game with.
- `curl http://127.0.0.1:5000/questions?quizzes -X POST -H "Content-Type: application/json" -d '{'previous_questions': [1, 4, 20, 15],"quiz_category': 0}`
```
{
  "questions": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": true
}
```


## Deployment N/A

## Author
 Abdulaziz Saad

## Acknowledgements 
I really want to commend Merry Blessing for believing in me.

