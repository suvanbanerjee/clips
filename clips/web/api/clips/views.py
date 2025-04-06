from typing import List, Optional
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.responses import RedirectResponse

from clips.db.dao.clip_dao import ClipDAO
from clips.db.models.clip_model import ClipModel
from clips.web.api.clips.schema import (
    ClipDTO,
    ClipInputDTO,
    ClipStatsDTO,
)

router = APIRouter()


@router.get("/", response_model=List[ClipDTO])
async def get_clips(
    limit: int = Query(20, description="Maximum number of clips to return"),
    offset: int = Query(0, description="Number of clips to skip"),
    search: Optional[str] = Query(None, description="Search term"),
    clip_dao: ClipDAO = Depends(),
) -> List[ClipModel]:
    """
    Retrieve all clips from the database.

    :param limit: Maximum number of clips to return
    :param offset: Number of clips to skip
    :param search: Optional search term to filter clips
    :param clip_dao: DAO for clip models
    :return: List of clip objects from database
    """
    if search:
        return await clip_dao.search_clips(query=search, limit=limit, offset=offset)
    return await clip_dao.get_all_clips(limit=limit, offset=offset)


@router.get("/{clip_id}/stream")
async def stream_clip(
    clip_id: int = Path(..., description="The ID of the clip to stream"),
    clip_dao: ClipDAO = Depends(),
) -> RedirectResponse:
    """
    Stream audio file for a specific clip. Redirects to URL for remote files.

    :param clip_id: ID of the clip to stream
    :param clip_dao: DAO for clip models
    :return: Audio file response or redirect to remote URL
    :raises HTTPException: If clip not found
    """
    clip = await clip_dao.get_clip_by_id(clip_id=clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")

    # Increment play count
    await clip_dao.increment_play_count(clip_id=clip_id)

    # Parse URL to check if it's a remote URL
    parsed_url = urlparse(clip.url)
    if parsed_url.scheme in ["http", "https"]:
        # Return HTTP redirect to the remote URL
        return RedirectResponse(url=clip.url)
    return None


@router.get("/{clip_id}/stats", response_model=ClipStatsDTO)
async def get_clip_stats(
    clip_id: int = Path(..., description="The ID of the clip to get stats for"),
    clip_dao: ClipDAO = Depends(),
) -> ClipStatsDTO:
    """
    Get statistics for a specific clip.

    :param clip_id: ID of the clip
    :param clip_dao: DAO for clip models
    :return: Clip statistics
    :raises HTTPException: If clip not found
    """
    clip = await clip_dao.get_clip_by_id(clip_id=clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")

    # Return clip with its statistics
    return {
        "id": clip.id,
        "title": clip.name,
        "description": clip.description,
        "genre": clip.tags[0] if clip.tags else None,
        "duration": clip.duration,
        "play_count": clip.play_count,
        "created_at": clip.created_at,
        "updated_at": clip.updated_at,
    }


@router.post("/", response_model=ClipDTO)
async def create_clip(
    clip_input: ClipInputDTO,
    clip_dao: ClipDAO = Depends(),
) -> ClipModel:
    """
    Create a new clip entry in the database.

    :param clip_input: Clip data to create
    :param clip_dao: DAO for clip models
    :return: Created clip object
    """
    return await clip_dao.create_clip(
        name=clip_input.name,
        description=clip_input.description,
        url=clip_input.url,
        tags=clip_input.tags,
        duration=clip_input.duration,
    )
