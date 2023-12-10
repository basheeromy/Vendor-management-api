# Vendor-management-api
Vendor Management API

This repository contains the code for a Vendor Management API designed
to handle various vendor-related operations.

API Documentation.

The API endpoints and their functionalities are thoroughly documented
using Swagger. You can explore and test the API endpoints interactively
using Swagger UI.

To access the API documentation, navigate to http://localhost:8000/api/docs
after running the application. This URL will direct you to the Swagger
interface where you can find detailed information about each endpoint,
request parameters, response formats, and even test the API functionality
directly within the interface.

Getting Started

1. Clone this repository.

    $ git clone https://github.com/basheeromy/Vendor-management-api.git

move to the cloned directory.

2. Setup virtual environment.

    $ python3 -m venv venv

    $ source venv/bin/activate

3. Set up the project dependencies.

    $ pip install -r requirements.txt

    Install development dependencies if needed.

    $ pip install -r requirements.dev.txt

4. Generate a new secret key.

here is a way to generate secret key

open terminal.

    $ python3

    >>> import secrets

    >>> print(secrets.token_urlsafe())

copy the generated secret key

    >>> exit()

4. Move to project directory.

    $ cd vendor_app

5. Create .env file in the project root directory.(where settings.py file exists)
and paste SECRET_KEY=<secret_key>

6. apply migrations ( move to the directory which includes manage.py file )

    $ python manage.py makemigrations

    $ python manage.py migrate

7. create super user to access admin interface.

    $ python manage.py createsuperuser

8. use the bellow given command to run the server.

    $ python manage.py runserver

By incorporating efficient unit tests into our application,
we're equipped to execute them using the following command:

    $ python manage.py test

If we have installed the dev dependencies, we can use linting tool
with the help of following command to check pep8 standard.

    $ flake8

Run the application.

Details of Dependencies.

python version 3.11.6

Framework ~ Django==4.2.7

Following are the libraries and packages used in this api application.

django-cors-headers==4.3.1,

django-debug-toolbar==4.2.0,

django-filter==23.4,

djangorestframework==3.14.0,

djangorestframework-simplejwt==5.3.0,

drf-spectacular==0.26.5,  (swagger)

Faker==20.1.0, (we used to generate random texts in specific format.)

flake8==6.1.0, (linting tool.
see .flake8 file in django application's root directory.
use flake8 command on cli to check pep8 standard.)

python-dotenv==1.0.0


----------------------------------


Access http://localhost:8000/api/docs to explore the API documentation.
Feel free to use this API to manage vendors efficiently!


Order Related API endpoints.
![Swagger_Order](./images/swagger.png)

Vendor Related API endpoints.
![Swagger_Vendor](./images/swagger2.png)
