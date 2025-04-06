from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from loguru import logger
from piccolo.conf.apps import Finder
from piccolo.table import create_tables
from prometheus_fastapi_instrumentator.instrumentation import (
    PrometheusFastApiInstrumentator,
)

from clips.db.dao.clip_dao import ClipDAO
from clips.services.db_seeder import DatabaseSeeder


def setup_prometheus(app: FastAPI) -> None:  # pragma: no cover
    """
    Enables prometheus integration.

    :param app: current application.
    """
    PrometheusFastApiInstrumentator(should_group_status_codes=False).instrument(
        app,
    ).expose(app, should_gzip=True, name="prometheus_metrics")


@asynccontextmanager
async def lifespan_setup(
    app: FastAPI,
) -> AsyncGenerator[None, None]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    app.middleware_stack = None
    setup_prometheus(app)
    app.middleware_stack = app.build_middleware_stack()

    # Create database tables if they don't exist
    try:
        logger.info("Ensuring database tables exist...")
        tables = Finder().get_table_classes()
        create_tables(*tables, if_not_exists=True)
        logger.info("Database tables created or already exist")

        # Now check if database needs to be seeded
        logger.info("Checking if database needs to be seeded...")
        clip_dao = ClipDAO()
        seeder = DatabaseSeeder(clip_dao)

        if await seeder.is_database_empty():
            logger.info("Database is empty. Seeding with sample data...")
            await seeder.seed_sample_data()
            logger.info("Database seeding completed successfully.")
        else:
            logger.info("Database already contains data. Skipping seed operation.")
    except Exception as e:
        logger.error(f"Error during database initialization/seeding: {e!s}")

    yield
