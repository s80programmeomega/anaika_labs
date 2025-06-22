# anaika_labs

A solution to the french pronunciation evaluation of the [SeyGe](https://seyge.netlify.app) app from [Anaika_labs](
    https://anakailabs.com
).

## How To Start The Server

### 1. Install python into your system

Download an install [Python](https://www.python.org/downloads/).
The required python version is 3.10 upward.
Make sure python is availble on your system path.

### 2. Create a virtual environment

Open a command prompt or a terminal and 

    cd inot/your/desired/location/

and execute this commad:

    python -m venv .venv

### 3. Activate it

#### - Activation for Windows users

     .venv\Scripts\activate 

#### - Activation for Linux users

     source .venv/bin/activate 

### 4 Clone this project locally

Download and install [Git](https://github.com/s80programmeomega/anaika_labs.git)
, and make sure it is available in your system path.
Clone this repository using: 

     git clone https://github.com/yourusername/anaika_labs.git 

Then:

     cd into/the/project/directory 

### 5 Install the requirements

Navigate to the project directory and run:

     pip install -r requirements.txt 

### 6 Create a superuser

     python manage.py createsuperuser 

### 7 Lunch the server

Run the Django development server:

    python manage.py runserver

### 8 Test the back-end

#### - Test your API endpoints using Postman or cURL.

API Root: 

    http:localhost:8000

Admin panel:
    
    http:localhost:8000/admin

#### - Api documentation

##### -- Swager-ui

    http://localhost:8000/api/schema/swagger-ui/

##### -- Redoc

    http://localhost:8000/api/schema/redoc/
