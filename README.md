# PythonFlaskRESTAPI
REST API implemented in Python using the Flask library

## Prerequisites
* [Python 3.9](https://www.python.org/downloads/release/python-390/) should be installed on your system.
* docker or a an available SQL server

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

### Run PostgeSQL in Docker
* In this example we will use PostgreSQL in Docker. If you already have a DB installed or access to a DB server, you can skip this section.
* Pull the PostgreSQL image from Docker Hub.
  ```cmd
  docker pull postgres
  ```
* Run the pulled image as a container.
  ```cmd
  docker run -d -p 5432:5432 --name postgres -e POSTGRES_USER=pguser -e POSTGRES_PASSWORD=secret_key -e POSTGRES_DB=demo_db postgres
  ```
  
### Connecting to a DB using [SQLAlchemy ORM](https://www.sqlalchemy.org/)
* SQLAlchemy is a Python ORM that allows you to connect to a database and query it.
* Object-Relational Mapping (ORM) is a technique that lets you query and manipulate data from a database using an object-oriented paradigm.
* ORM libraries usually allows the developer to hide the complexities of using a database.

* Add the `flask_sqlalchemy` and [`psycopg2`](https://www.psycopg.org/docs/) package to the requirements.txt file and install it using `pip install -r requirements.txt`
* [`psycopg2`](https://www.psycopg.org/docs/) is a Python module that allows you to connect to a PostgreSQL database. For other types of database servers you will need other connectors.

* In the config file add the database connection string. Notice that you can have different connection strings in the test and default configuration file:
```
        self.SQLALCHEMY_DATABASE_URI = 'postgresql://pguser:secret_key@localhost:5432/demo_db'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
```
* The SQLALCHEMY_TRACK_MODIFICATIONS will track modifications of objects and emit signals if it's set to True. Since we will not use signals 
    we can set it to False.

* Crete a database.py file to initiate a SQLAlchemy database object and add the following code inside:
```python
  from flask_sqlalchemy import SQLAlchemy
  db = SQLAlchemy()
```

* In the `app.py` file import the database object
```python
  from database import database
```

* Then initialize an application for the use with the database setup
```python
  database.init_app(app)
```
### Database model
* In the api folder create a folder called `models`. This will hold the application models.
* Create a file called `random_value.py`.
* Import the `sqalchemy` library and the `database` object from the `database.py` file.
```python
    import sqlalchemy
    from Database import database
```
* Create a model class. The class properties will be sqlalchemy Column objects.
```python
    class RandomValue(database.Model):
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
        date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.now())
        value = sqlalchemy.Column(sqlalchemy.Integer)
```

### Database migrations
* Add the `flask_migrate` package to the requirements.txt file and install it using `pip install -r requirements.txt`
* In the `app.py` file import the `flask_migrate` package.
```python
  from flask_migrate import Migrate
```
* Then initialize the migrations engine.
```python
  Migrate(app, database)
```
* In the `app.py` import the `RandomValue` model class so the migrations engine can generate dabase tables for it.
```python
  from models.random_value import RandomValue
```
* In the console run the `flask db init` command to create the migrations folder.
* In the console run the `flask db migrate -m "Initial migration"` command to create the initial migration.
* You can inspect the generated migration query in the `migrations\versions` folder.
* Apply the migration by running the `flask db upgrade` command.


### [Dependency Injection](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) in a class
* The same database instance will have to be injected in the constructor of other classes.
* In the `requirements.txt` add the `flask-injector` package and install it using `pip install -r requirements.txt`

* In the `create_app` frunction from `api.py` define the function that will configure the desired dependencies.
```python
  import flask_injector
    ...
  def configure_dependencies(binder):
    binder.bind(SQLAlchemy, to=database, scope=flask_injector.singleton)
```
* The code above will bind the `SQLAlchemy` class to the `database` object. So everytime the `SQLAlchemy` class is requested it will return the same instance of the `database` object.

* Now set the function above as a callback for the FlaskInjector. This has to be but after registering the blueprints.
```python
  flask_injector.FlaskInjector(app=app, modules=[configure_dependencies])
```

### Repository service
* Add a `api/services` folder to hold the service classes.
* Create the `api/services/random_value_repository.py` file.
* Import the required library for the dependency injection.
```python
    from flask_sqlalchemy import SQLAlchemy
    from flask_injector import inject
```
* And defined the class `RandomValueRepository` that will be used to interact with the database.
```python
    class RandomValueRepository:
        @inject
        def __init__(self, database: SQLAlchemy):
            self.__database = database
```

* We use the `inject` decorator to inject the `database` singleton object into the constructor of the `RandomValueRepository` class.

### Data transfer object
* Let's also add a [data transfer object (DTO)](https://www.baeldung.com/java-dto-pattern) model to be used for the interactions with the client.
* A DTO is a good idea because 
  * it decouples the database model from the object used to interact with the client.
  * it encapsulates of the serialization's logic sice the data will be serialized when sent over http.
  * can reduce roundtrips to the server by batching up multiple parameters in a single call. 
* Create the `api/models/random_value_collection.py` file and define the following class inside:
```python
class RandomValueCollection:
    def __init__(self, values: [], page: int, pageSize: int, totalNumberOfItems: int):
        self.values = values
        self.page = page
        self.pageSize = pageSize
        self.numberOfPages = math.ceil(float(totalNumberOfItems) / float(pageSize))
```
* Create the `api/models/random_value_transfer_object.py` file and define the following class inside:
```python
class RandomValueTransferObject:
    def __init__(self, date= None, value= None):
        self.date = date
        self.value = value
```
* We skipped the `id` property because it is not needed by the client.

### Mappers
* We will also need a function to map between the database model and the DTO.  
So create the file `api/services/random_value_mapper.py` and define the following function inside:
```python
def random_value_to_transfer_object(dbo):
    transferObject = RandomValueTransferObject()
    transferObject.date = dbo.date
    transferObject.value = dbo.value
    return transferObject
```
* Add the function to map a transfer object to a database object.
```python
def transfer_object_to_random_value(transferObject):
    dbo = RandomValue()
    dbo.date = transferObject.date
    dbo.value = transferObject.value
    return dbo
```

### Repository service getter
* In the `RandomValueRepository` class create the  `save` method that will save the random value to the database.
```python
    def save(self, newValue: RandomValueTransferObject):
        dbo = transfer_object_to_random_value(newValue)
        self.__database.session.add(dbo)
        self.__database.session.commit()
        return random_value_to_transfer_object(dbo)
```

* In the `RandomValueRepository` class create the `get_all` method that will retrieve the random value from the database.
```python
    def get_all(self, page: int, pageSize: int):
        totalNumberOfItems = RandomValue.query.count()
        collection = RandomValue.query.paginate(page, pageSize, error_out=False)
        return RandomValueCollection(list(map(lambda dbo: random_value_to_transfer_object(dbo), collection.items)), page, pageSize, totalNumberOfItems)
```

### Dependency Injection in a route
* To implement the `save/value` and `get/values` routes we need to inject the `RandomValueRepository` class.
* In the `configure_dependencies` from `api.py` add the following line:
```python
  binder.bind(RandomValueRepository, to=RandomValueRepository, scope=flask_injector.singleton)
```

### The save and get routes
* In the `requirements.txt` add the `jsonpickle` package and install it using `pip install -r requirements.txt`. This is needed for serialization and deserialization of the DTO.

* Create the `api/controler/value.py` file to hold the new routes.
* In the `value.py` add the blueprint for the routes.
```python
  from flask import Blueprint
  value = Blueprint('value', __name__)
```

* And register the blueprint in the `app.py` file.
```python
  app.register_blueprint(value, url_prefix='/value')
```

* Now in the `value.py` file we can create the `save` route. Notice that the `RandomValueRepository` is injected in the method that is used to resolve the call to the endpoint.
```python
@value.route('/save', methods=['POST'])
def save(repository: RandomValueRepository):
    newVal = request.get_json()
    result = repository.save(RandomValueTransferObject(**newVal))
    return jsonpickle.encode(result, unpicklable=False), http.HTTPStatus.OK
```

* And the `get` route.
```python
@storage.route('/get/recipes', methods=['GET'])
def getRecipes(recipeRepository: RecipeRepository):

    parameterName = 'start'
    defaultStart = datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0)
    start = request.args.get(parameterName, default=defaultStart)

    parameterName = 'end'
    tomorrow = datetime.now() + timedelta(days=1)
    defaultEnd = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0, second=0)
    end = request.args.get(parameterName, default=defaultEnd)

    parameterName = 'page'
    try:
        page = int(request.args.get(parameterName, default=1))
    except ValueError:
        return f'Invalid parameter {parameterName}', http.HTTPStatus.BAD_REQUEST

    parameterName = 'pageSize'
    try:
        pageSize = int(request.args.get(parameterName, default=10))
    except ValueError:
        return f'Invalid parameter {parameterName}', http.HTTPStatus.BAD_REQUEST

    result = recipeRepository.getByDate(start, end, page, pageSize)
    return jsonpickle.encode(result, unpicklable=False), http.HTTPStatus.OK
```
