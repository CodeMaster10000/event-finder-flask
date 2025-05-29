# Event Finder

A Flask-based backend for the **Event Finder** application, providing a RESTful API to manage users and events with full CRUD support,
authentication, dependency injection and AI support.

## Features

- **User Management**: Signup, login, logout, and profile retrieval
- **Event Management**: Create, list, retrieve, update, and delete events
- **Guest Invitations**: Add and remove guests from events
- **Authentication**: JWT-based guard for protected endpoints
- **Serialization**: Marshmallow schemas for clean request/response modeling
- **Dependency Injection**: `dependency-injector` for wiring controllers and services
- **AI Support**: `ollama` and `OpenAI` for dynamic event retrieval and embedding
## Technologies & Dependencies

- **Flask**: Web framework (3.1.0)
- **Flask-SQLAlchemy**: ORM integration (SQLAlchemy 2.0.40)
- **Flask-JWT-Extended**: JWT authentication (PyJWT 2.10.1)
- **Flask-Bcrypt**: Password hashing (bcrypt 4.3.0)
- **marshmallow** & **marshmallow-sqlalchemy**: Schema-based (de)serialization
- **dependency-injector**: Service and controller wiring
- **pgvector**: Vector extension for PostgreSQL, used for RAG
- **OpenAI** SDK for cloud embeddings and chat  
- **sentence-transformers** 4.1.0, **transformers** 4.52.3 & **torch** 2.7.0 for local embeddings  
- **Ollama** CLI for local LLM completions 

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

#### After installing poetry, you might have to open a new terminal

  ```bash
    pip install poetry
    poetry install
  ```

### 4. Configure environment variables

Create a `.env` and a `.flaskenv` file in the project root:

#### .env
```dotenv
# Postgres credentials
DATABASE_URL=postgresql://event_user:event_pass@localhost:5432/event_db

# Ports
DB_PORT=5432
WEB_PORT=5000

#Embeddings
VECTOR_DIM=1536
MODEL_TYPE=local
CLOUD_MODEL_API_KEY=xxx
CLOUD_MODEL_EMBEDDER_NAME=text-embedding-ada-002
LOCAL_MODEL_NAME=llama3.2-vision
LOCAL_MODEL_EMBEDDER_NAME=sentence-transformers/all-mpnet-base-v2
```

#### .flaskenv
```dotenv
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${DB_PORT}/${POSTGRES_DB}"

```
> **Note**: If Postgres runs in Docker with `ports: "5432:5432"`, set `localhost:5432`. Otherwise, use your container host.

### 5. Run database migrations

 Start the database via docker-compose
```bash
  docker-compose up db    
```

 Run the migrations
```bash
  flask db upgrade     # apply to the database
```

### 6. Start the application

  - If you want **Local AI support**, make sure to have `MODEL_TYPE = local` in .**env**,
  otherwise set it to `MODEL_TYPE = cloud` to use OpenAI. Have **Ollama started, up and running** locally!
  **The application does not start ollama for you, only the model... that is, if you have it!**
  - For **cloud**, make sure to get an **API_KEY** from https://platform.openai.com/account/api-keys.
    You might have to upgrade the billing plan—nothing comes free.

```bash
  flask run
```
 Or via Docker Compose

 First, build the image, then run via docker-compose
```bash
  docker build -t event-finder:0.0.1 .    
  docker-compose up web
```

Visit [http://localhost:\${WEB\_PORT}/swagger/](http://localhost:${WEB_PORT}/swagger/) for Swagger UI and to explore the REST API.

## License

This project has no License

---

*Maintained by Mile Stanislavov*
