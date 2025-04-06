# Soundverse Backend Assignment

Task was to build a backend service for a fictitious feature called "Clips" — a lightweight audio library that lets users fetch and stream short audio previews. goal is to implement basic API functionality, integrate a database, and deploy it online with simple monitoring

To go about this project I first setup a boilerplate code, for that i used [fastapi-template](https://pypi.org/project/fastapi_template/)

## What is implied in this project

- API route to get all clips
- API route to get a clip by id
- API route to stream a clip
- API route to POST a new clip 

## Setup Project Locally

### Docker (Recomended)

You can start the project with docker using this command:

```bash
docker-compose up --build
```

### Using Poetry

This project uses poetry. It's a modern dependency management tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m clips
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Project structure
```bash
clips
├── __init__.py
├── __main__.py  # Startup script
├── log.py  # Logging configuration
├── piccolo_conf.py  # Database configuration
├── settings.py  # Main configuration settings
├── db  # Database module
│   ├── app_conf.py  # Database application configuration
│   ├── dao  # Data Access Objects
│   │   ├── __init__.py
│   │   └── clip_dao.py  # DAO for clip operations
│   └── models  # Database models
│       ├── __init__.py
│       └── clip_model.py  # Model for clip data
├── services  # External services
│   ├── __init__.py
│   └── db_seeder.py  # Database seeding service
├── static  # Static content
└── web  # Web server package
    ├── __init__.py
    ├── application.py  # FastAPI application configuration
    ├── lifespan.py  # Startup and shutdown actions
    └── api  # API handlers
        ├── __init__.py
        ├── router.py  # Main router
        └── clips  # Clips specific API
            ├── __init__.py
            ├── schema.py  # Pydantic schemas for clips
            └── views.py  # API endpoints for clips
```

The project follows a clean architecture with separated layers for:
- Web API (routing and endpoints)
- Database access (models and DAOs)
- Services (business logic)
- Configuration and settings

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. 

All environment variables should start with "CLIPS_" prefix.

For example if you see in your "clips/settings.py" a variable named like
`random_parameter`, you should provide the "CLIPS_RANDOM_PARAMETER" 
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `clips.settings.Settings.Config`.

An example of .env file:
```bash
CLIPS_RELOAD="True"
CLIPS_PORT="8000"
CLIPS_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Database
It was only mentioned to use PostgreSQL but as per the doc we are suposed to use it like a production application hence i have used Pinacco as ORM to make it more easy to deal with database opperations

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* ruff (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/


## Running tests

If you want to run it in docker, simply run:

```bash
pytest
```
the test are divided in two folders 
- test_api
- test_db

In total there are 10 test to cover the most basic opps