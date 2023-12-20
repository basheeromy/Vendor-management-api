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

<h3>Clone this repository.</h3>

git clone https://github.com/basheeromy/Vendor-management-api.git

move to the cloned directory.

<h4>Setup virtual environment.</h4>

    python3 -m venv venv

source venv/bin/activate

<h4>Set up the project dependencies.</h4>

    pip install -r requirements.txt

<h4>Install development dependencies if needed.</h4>

    pip install -r requirements.dev.txt

<h4>Generate a new secret key.</h4>

here is a way to generate secret key

open terminal.

    python3

    >>> import secrets

    >>> print(secrets.token_urlsafe())

<h4>copy the generated secret key</h4>

    >>> exit()

<h4>Move to project directory.</h4>

    cd vendor_app

Create .env file in the project root directory.(where settings.py file exists)
and paste SECRET_KEY=<secret_key>

<h4>Apply migrations</h4> ( move to the directory which includes manage.py file )

    python manage.py makemigrations

    python manage.py migrate

<h4>Create super user to access admin interface.</h4>

    python manage.py createsuperuser

<h4>Use the bellow given command to run the server.</h4>

    python manage.py runserver

<h4>Unit tests </h4> By incorporating efficient unit tests into our application,
we're equipped to execute them using the following command:

    python manage.py test

<h4>Linting</h4> If we have installed the dev dependencies, we can use linting tool
with the help of following command to check pep8 standard.

    flake8

Details of Dependencies.

Python version 3.11.6

Framework ~ Django==4.2.7



----------------------------------


Access http://localhost:8000/api/docs to explore the API documentation.
Feel free to use this API to manage vendors efficiently!


Order Related API endpoints.
![Swagger_Order](./images/swagger.png)

Vendor Related API endpoints.
![Swagger_Vendor](./images/swagger2.png)
