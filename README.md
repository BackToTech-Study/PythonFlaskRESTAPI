# PythonFlaskRESTAPI
REST API implemented in Python using the Flask library

## Prerequisites
* [Python 3.9](https://www.python.org/downloads/release/python-390/) should be installed on your system.

## Setup the project - [https://flask.palletsprojects.com/en/2.1.x/installation/](https://flask.palletsprojects.com/en/2.1.x/installation/)
* create the virtual environment
  ```
    python3.9 -m venv venv
  ```
* activate the virtual environment
  ```
    venv/bin/activate.bat
  ```
* create a file named `requirements.txt` in the root directory of the project and add `flask` to the list of dependencies

* install requirements
  ```
    pip install -r requirements.txt
  ```

## Implementation
### [Application Factory](https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/)
* if you move the creation of this object into a function, you can then create multiple instances of this app later.
* So why would you want to do this?
  * Testing. You can have instances of the application with different settings to test every case.
  * Multiple instances. 
    * Imagine you want to run different versions of the same application. 
    * You could have multiple instances with different configs set up in your webserver, but if you use factories, 
    * you can have multiple instances of the same application running in the same application process which can be handy.
* Flask will automatically detect the factory functions that are named `create_app` or `make_app`

### The Flask app
* we've implemented the application factory function in the file `app.py`
* to run the application in a flask development server execute `flask run` in a console
* you can instruct flask to run in the development environment by setting the environment variable `FLASK_ENV` to `development`
  ```cmd
  set FLASK_ENV=development
  ```
* Running in debug mode will automatically reload the server if a source file changes.

### [Blueprints](https://flask.palletsprojects.com/en/2.1.x/blueprints/)
* Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications.
* The basic concept of blueprints is that they record operations to execute when registered on an application.

### Routing and endpoints
* In the controller file create a blueprint variable that you can register later on the application.
```
  from flask import Blueprint
  status = Blueprint('status', __name__)
```
* You can bind a function to a route by using the blueprint name and the route decorator.
```
    @status.route('/now', methods=['GET'])
    def echo():
        return str(datetime.now()), http.HTTPStatus.OK
```
* Then register the blueprint on the application factory function.
```
  app.register_blueprint(status, url_prefix='/status')
```
* The url prefix is the path that the blueprint will be registered on.
* Now the `/status/now` route will be available.

### App configurations
* You can pass an argument to the application factory function to set the config file name. Or a keyword in our case. 
  To do this set the value of the `FLASK_APP` environment variable like so:
  ```bash
    set FLASK_APP=app:create_app('development')
  ```
  Where `app` is the name of the file that holds the factory function and `create_app` is the name of the factory function.

* Then run the `flask run` command.

* In the factory function you could then import the appropriate config class or load the config file.
  ```python
  if configuration_key == 'development':
    from test_configuration import TestConfiguration as Configuration
  else:
    from configuration import Configuration as Configuration
  ```
* Then you cand use the `app.config.from_file` function to load a config file or use `from_object` to load a config class.
  ```python
  app.config.from_object(Configuration())
  ```
* There are also options for loading configurations from environment variables, python files, mappings ... .

### Connecting to a DB using SQLAlchemy ORM
### Database model
### Database migrations
### Repository service
### Dependency Injection in a class
### Dependency Injection in a route
### Data Transfer Object
### Mappers
### Adding CORS
