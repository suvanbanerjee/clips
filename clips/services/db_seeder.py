import logging
from pathlib import Path
from typing import Optional

from clips.db.dao.clip_dao import ClipDAO

logger = logging.getLogger(__name__)


class DatabaseSeeder:
    """Service to check if the database is empty and seed it with sample data."""

    def __init__(self, clip_dao: ClipDAO) -> None:
        """Initialize the database seeder with DAOs."""
        self.clip_dao = clip_dao

    async def is_database_empty(self) -> bool:
        """Check if the database is empty (no clips)."""
        clips = await self.clip_dao.get_all_clips(limit=1)
        return len(clips) == 0

    async def seed_sample_data(self, samples_dir: Optional[Path] = None) -> None:
        """
        Seed the database with sample clip data.

        :param samples_dir: Optional directory containing sample audio files
        """
        logger.info("Seeding database with sample clip data")

        sample_clips = [
            {
                "name": "Without Me",
                "description": "A song by Halsey",
                "url": "https://samplesongs.netlify.app/Without%20Me.mp3",
                "duration": 200,
                "tags": "pop,song,halsey",
            },
            {
                "name": "Death Bed",
                "description": "A song by Powfu",
                "url": "https://samplesongs.netlify.app/Death%20Bed.mp3",
                "duration": 210,
                "tags": "pop,song,powfu",
            },
            {
                "name": "Bad Liar",
                "description": "A song by Imagine Dragons",
                "url": "https://samplesongs.netlify.app/Bad%20Liar.mp3",
                "duration": 260,
                "tags": "rock,song,imagine dragons",
            },
            {
                "name": "Faded",
                "description": "A song by Alan Walker",
                "url": "https://samplesongs.netlify.app/Faded.mp3",
                "duration": 212,
                "tags": "electronic,song,alan walker",
            },
            {
                "name": "Hate Me",
                "description": "A song by Ellie Goulding",
                "url": "https://samplesongs.netlify.app/Hate%20Me.mp3",
                "duration": 190,
                "tags": "pop,song,ellie goulding",
            },
            {
                "name": "Solo",
                "description": "A song by Clean Bandit",
                "url": "https://samplesongs.netlify.app/Solo.mp3",
                "duration": 222,
                "tags": "pop,electronic,clean bandit",
            },
        ]

        # Insert each sample clip into the database
        for clip_data in sample_clips:
            await self.clip_dao.create_clip(
                name=clip_data["name"],
                description=clip_data["description"],
                url=clip_data["url"],
                duration=clip_data["duration"],
                tags=clip_data["tags"],
            )

        logger.info(
            f"Successfully added {len(sample_clips)} sample clips to the database",
        )
