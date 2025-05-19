# Event Finder

A Flask-based backend for the **Event Finder** application, providing a RESTful API to manage users and events with full CRUD support, authentication, and dependency injection.

## Features

* **User Management**: Signup, login, logout, and profile retrieval
* **Event Management**: Create, list, retrieve, and delete events
* **Guest Invitations**: Add guests to events
* **Authentication**: JWT-based guard for protected endpoints
* **Serialization**: Marshmallow schemas for clean request/response modeling
* **Dependency Injection**: `dependency-injector` for wiring controllers and services

## Technologies & Dependencies

* **Flask**: Web framework for Python 3.1.0
* **Flask-SQLAlchemy**: ORM integration (SQLAlchemy 2.0.40)
* **Flask-JWT-Extended**: JWT authentication (PyJWT 2.10.1)
* **Flask-Bcrypt**: Password hashing via bcrypt 4.3.0
* **marshmallow** & **marshmallow-sqlalchemy**: Schema-based (de)serialization
* **dependency-injector**: Service and controller wiring

Other dependencies:

```
bcrypt==4.3.0
blinker==1.9.0
click==8.1.8
colorama==0.4.6
dependency-injector==4.46.0
Flask==3.1.0
Flask-Bcrypt==1.0.1
Flask-JWT-Extended==4.7.1
flask-marshmallow==1.3.0
Flask-SQLAlchemy==3.1.1
greenlet==3.2.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
marshmallow==4.0.0
marshmallow-sqlalchemy==1.4.2
PyJWT==2.10.1
SQLAlchemy==2.0.40
typing_extensions==4.13.2
Werkzeug==3.1.3
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CodeMaster10000/event-finder-flask.git
   cd event-finder-flask
   ```
2. Create a virtual environment and install requirements:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure your database URI and JWT secret in `config.py` or environment variables.
4. Run the app:

   ```bash
   flask run
   ```

## API Documentation

After starting the server, browse to [http://localhost:5000/swagger/](http://localhost:5000/swagger/) to view the Swagger UI and test endpoints.

---

*Mile Stanislavov*
