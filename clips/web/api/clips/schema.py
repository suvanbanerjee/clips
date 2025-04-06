from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClipDTO(BaseModel):
    """
    DTO for clip models.

    It returned when accessing clip models from the API.
    """

    id: int
    name: str
    url: str
    description: Optional[str] = None
    duration: Optional[int] = None
    play_count: int
    tags: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClipStatsDTO(BaseModel):
    """
    DTO for clip statistics.

    It returned when accessing clip statistics from the API.
    """

    id: int
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    duration: Optional[int] = None
    play_count: int
    created_at: datetime
    updated_at: datetime


class ClipInputDTO(BaseModel):
    """DTO for creating new clip."""

    name: str
    url: str
    description: Optional[str] = None
    duration: Optional[int] = None
    tags: Optional[str] = None


class ClipUpdateDTO(BaseModel):
    """DTO for updating an existing clip."""

    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    tags: Optional[str] = None
