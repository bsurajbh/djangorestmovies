# djangorestmovies
REST API implementation for movies, ratings, comments

##Getting started
Setup

    # clone this repository
   
    python3 -m venv restmovies
    . restmovies/bin/activate
    cd djangorestmovies
    pip3 install -r requirements.txt
    python3 manage.py runserver

APIs    
    
    # register
    http://localhost:8000/api/users/register/
    # login 
    http://localhost:8000/api/users/login/
    # movies list
    http://localhost:8000/api/movies/
    # movie details
    http://localhost:8000/api/movies/45/
    # fedback
    http://localhost:8000/api/feedback/
    # logout
    http://localhost:8000/api/users/logout/
    
    # Admin Login
    http://localhost:8000/admin/
    username: admin
    password: admin
     
Test
    
    python3 manage.py test     
    
###Note

* Repository has includes test database with test data
* Data is generated with Faker so it might be not relevent to what it means in context.
* While using postman please include { Authorization : Token <your valid token>} in header

* Includes management command to generate test data using faker factory

        python3 manage.py dbseed 5
        # can terminate if data contraints prevails
* Refer __factories.py__ to make changes in data seeding pattern.
        


 