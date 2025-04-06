import pytest
from httpx import AsyncClient

from clips.db.dao.clip_dao import ClipDAO


@pytest.mark.anyio
async def test_create_clip(client: AsyncClient) -> None:
    """Test creating a new clip via API."""
    # Define test clip data
    test_clip = {
        "name": "Test Song",
        "description": "A test song for API",
        "url": "https://example.com/test.mp3",
        "duration": 180,
        "tags": "test,api,song",
    }

    # Make API request to create clip
    response = await client.post("/api/clips/", json=test_clip)

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_clip["name"]
    assert data["description"] == test_clip["description"]
    assert data["url"] == test_clip["url"]
    assert data["duration"] == test_clip["duration"]
    assert data["tags"] == test_clip["tags"]
    assert data["play_count"] == 0
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.anyio
async def test_get_all_clips(client: AsyncClient, clip_dao: ClipDAO) -> None:
    """Test getting all clips via API."""
    # Create test clips in database
    clip1 = await clip_dao.create_clip(
        name="Test Song 1",
        description="The first test song",
        url="https://example.com/song1.mp3",
        duration=180,
        tags="test,first",
    )

    clip2 = await clip_dao.create_clip(
        name="Test Song 2",
        description="The second test song",
        url="https://example.com/song2.mp3",
        duration=200,
        tags="test,second",
    )

    # Get all clips via API
    response = await client.get("/api/clips/")

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    # Verify clips are in response
    clip_ids = [clip["id"] for clip in data]
    assert clip1.id in clip_ids
    assert clip2.id in clip_ids


@pytest.mark.anyio
async def test_search_clips(client: AsyncClient, clip_dao: ClipDAO) -> None:
    """Test searching for clips via API."""
    # Create clips with different tags
    await clip_dao.create_clip(
        name="Rock Song",
        description="A rock test song",
        url="https://example.com/rock.mp3",
        duration=180,
        tags="rock,test",
    )

    await clip_dao.create_clip(
        name="Pop Song",
        description="A pop test song",
        url="https://example.com/pop.mp3",
        duration=200,
        tags="pop,test",
    )

    # Search for rock clips
    response = await client.get("/api/clips/", params={"search": "rock"})

    # Verify response
    assert response.status_code == 200
    data = response.json()

    # Verify only rock songs are returned
    assert len(data) >= 1
    assert all("rock" in clip["tags"].lower() for clip in data)
    assert not any(
        "pop" in clip["name"].lower() and "rock" not in clip["tags"].lower()
        for clip in data
    )


@pytest.mark.anyio
async def test_get_clip_stats(client: AsyncClient, clip_dao: ClipDAO) -> None:
    """Test getting clip statistics via API."""
    # Create a test clip
    test_clip = await clip_dao.create_clip(
        name="Stats Test Song",
        description="A song to test statistics",
        url="https://example.com/stats.mp3",
        duration=240,
        tags="test,stats",
    )

    # Get clip stats via API
    response = await client.get(f"/api/clips/{test_clip.id}/stats")

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_clip.id
    assert data["title"] == test_clip.name
    assert data["description"] == test_clip.description
    assert data["duration"] == test_clip.duration
    assert data["play_count"] == 0


@pytest.mark.anyio
async def test_stream_clip_increments_plays(
    client: AsyncClient,
    clip_dao: ClipDAO,
) -> None:
    """Test that streaming a clip increments play count."""
    # Create a test clip
    test_clip = await clip_dao.create_clip(
        name="Stream Test Song",
        description="A song to test streaming",
        url="https://samplesongs.netlify.app/Faded.mp3",
        duration=212,
        tags="test,stream",
    )

    # Initial play count should be 0
    initial_clip = await clip_dao.get_clip_by_id(test_clip.id)
    assert initial_clip
    assert initial_clip.play_count == 0

    # Stream the clip
    await client.get(f"/api/clips/{test_clip.id}/stream")

    # Check play count was incremented
    updated_clip = await clip_dao.get_clip_by_id(test_clip.id)
    assert updated_clip
    assert updated_clip.play_count == 1


@pytest.fixture
async def clip_dao() -> ClipDAO:
    """Fixture for ClipDAO."""
    return ClipDAO()
