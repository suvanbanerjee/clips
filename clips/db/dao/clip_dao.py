from typing import Any, List, Optional

from clips.db.models.clip_model import ClipModel


class ClipDAO:
    """Class for accessing clip table."""

    async def create_clip(
        self,
        name: str,
        url: str,
        description: Optional[str] = None,
        duration: Optional[int] = None,
        tags: Optional[str] = None,
    ) -> ClipModel:
        """
        Add a new clip to the database.

        :param name: Name of the clip
        :param url: URL of the audio file
        :param description: Description of the clip
        :param duration: Duration in seconds
        :param tags: Comma-separated tags
        :return: Created clip instance
        """
        clip = ClipModel(
            name=name,
            url=url,
            description=description,
            duration=duration,
            tags=tags,
            play_count=0,
        )
        await ClipModel.insert(clip)

        # Return the created clip
        created_clips = (
            await ClipModel.objects()
            .where(
                (ClipModel.name == name) & (ClipModel.url == url),
            )
            .order_by(ClipModel.id, ascending=False)
            .limit(1)
        )

        return created_clips[0] if created_clips else None

    async def get_all_clips(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> List[ClipModel]:
        """
        Get all clips with pagination.

        :param limit: Maximum number of clips to return
        :param offset: Number of clips to skip
        :return: List of clip models
        """
        return (
            await ClipModel.objects()
            .order_by(
                ClipModel.created_at,
                ascending=False,
            )
            .limit(limit)
            .offset(offset)
        )

    async def get_clip_by_id(self, clip_id: int) -> Optional[ClipModel]:
        """
        Get a clip by its ID.

        :param clip_id: ID of the clip
        :return: Found clip or None
        """
        clips = await ClipModel.objects().where(ClipModel.id == clip_id)
        return clips[0] if clips else None

    async def update_clip(
        self,
        clip_id: int,
        **kwargs: Any,
    ) -> None:
        """
        Update a clip's details.

        :param clip_id: ID of the clip to update
        :param kwargs: Fields to update
        """
        await ClipModel.update(kwargs).where(ClipModel.id == clip_id)

    async def delete_clip(self, clip_id: int) -> None:
        """
        Delete a clip.

        :param clip_id: ID of the clip to delete
        """
        await ClipModel.delete().where(ClipModel.id == clip_id)

    async def increment_play_count(self, clip_id: int) -> None:
        """
        Increment the play count for a clip.

        :param clip_id: ID of the clip
        """
        clip = await self.get_clip_by_id(clip_id)
        if clip:
            await ClipModel.update(
                {
                    "play_count": clip.play_count + 1,
                },
            ).where(ClipModel.id == clip_id)

    async def search_clips(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
    ) -> List[ClipModel]:
        """
        Search for clips by name, description, or tags.

        :param query: Search query string
        :param limit: Maximum number of results
        :param offset: Number of results to skip
        :return: List of matching clips
        """
        return (
            await ClipModel.objects()
            .where(
                (ClipModel.name.ilike(f"%{query}%"))
                | (ClipModel.description.ilike(f"%{query}%"))
                | (ClipModel.tags.ilike(f"%{query}%")),
            )
            .order_by(
                ClipModel.play_count,
                ascending=False,
            )
            .limit(limit)
            .offset(offset)
        )
