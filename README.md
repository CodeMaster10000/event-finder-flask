# Event Finder

A Flask-based backend for the **Event Finder** application, providing a RESTful API to manage users and events with full CRUD support, authentication, and dependency injection.

## Features

- **User Management**: Signup, login, logout, and profile retrieval
- **Event Management**: Create, list, retrieve, update, and delete events
- **Guest Invitations**: Add and remove guests from events
- **Authentication**: JWT-based guard for protected endpoints
- **Serialization**: Marshmallow schemas for clean request/response modeling
- **Dependency Injection**: `dependency-injector` for wiring controllers and services

## Technologies & Dependencies

- **Flask**: Web framework (3.1.0)
- **Flask-SQLAlchemy**: ORM integration (SQLAlchemy 2.0.40)
- **Flask-JWT-Extended**: JWT authentication (PyJWT 2.10.1)
- **Flask-Bcrypt**: Password hashing (bcrypt 4.3.0)
- **marshmallow** & **marshmallow-sqlalchemy**: Schema-based (de)serialization
- **dependency-injector**: Service and controller wiring
- **pgvector**: Vector extension for PostgreSQL
- **OpenAI**: Embeddings & ChatCompletion for RAG

### Supplementary Libraries

```text
aniso8601==10.0.1
attrs==25.3.0
blinker==1.9.0
click==8.1.8
colorama==0.4.6
flask-restx==1.3.0
greenlet==3.2.1
gunicorn==23.0.0
importlib_resources==6.5.2
iniconfig==2.1.0
itsdangerous==2.2.0
Jinja2==3.1.6
jsonschema==4.23.0
jsonschema-specifications==2025.4.1
MarkupSafe==3.0.2
packaging==25.0
pluggy==1.6.0
python-dotenv==1.1.0
pytz==2025.2
referencing==0.36.2
rpds-py==0.24.0
typing_extensions==4.13.2
Werkzeug==3.1.3
dependency-injector==4.46.0
flask-marshmallow==1.3.0
Flask-SQLAlchemy==3.1.1
Flask-HTTPAuth==4.8.0
Flask-JWT-Extended==4.7.1
Flask-Bcrypt==1.0.1
marshmallow==4.0.0
marshmallow-sqlalchemy==1.4.2
openai==0.27.0
psycopg2-binary==2.9.7
pgvector==0.4.2
````

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/CodeMaster10000/event-finder-flask.git
cd event-finder-flask
```

### 2. Set up a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
```

### 3. Install dependencies

* **With Poetry** (recommended):

  ```bash
  poetry install
  poetry install --with testing
  ```

* **With pip**:

  ```bash
  pip install --upgrade pip setuptools wheel
  pip install -r requirements.txt
  ```

### 4. Configure environment variables

Create a `.env` and a `.flaskenv` file in the project root:

```dotenv
######.env######
# Postgres credentials
POSTGRES_USER=event_user
POSTGRES_PASSWORD=event_pass
POSTGRES_DB=event_db
DB_PORT=5432
WEB_PORT=5000

# Security & API keys
OPENAI_API_KEY=sk-...
VECTOR_DIM=1536
######.env######

# Flask & application settings - this goes in .flaskenv file
######.flaskenv######
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${DB_PORT}/${POSTGRES_DB}"
######.flaskenv######
```

> **Note**: If Postgres runs in Docker with `ports: "5432:5432"`, set `localhost:5432`. Otherwise, use your container host.

### 5. Run database migrations

```bash
flask db init        # only once
flask db migrate -m "Initial schema"
flask db upgrade     # apply to the database
```

### 6. Start the application

```bash
flask run            # or via Docker Compose
docker-compose up --build
```

Visit [http://localhost:\${WEB\_PORT}/swagger/](http://localhost:${WEB_PORT}/swagger/) for Swagger UI and to explore the REST API.

## License

This project is licensed under the MIT License.

---

*Maintained by Mile Stanislavov*

```
```
