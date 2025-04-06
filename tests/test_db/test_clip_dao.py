import pytest

from clips.db.dao.clip_dao import ClipDAO


@pytest.mark.anyio
async def test_create_and_get_clip() -> None:
    """Test creating and retrieving a clip from the database."""
    clip_dao = ClipDAO()

    # Create a test clip
    test_clip = await clip_dao.create_clip(
        name="Test Clip",
        description="A test clip",
        url="https://example.com/test.mp3",
        duration=180,
        tags="test,dao",
    )

    assert test_clip is not None
    assert test_clip.name == "Test Clip"
    assert test_clip.description == "A test clip"
    assert test_clip.url == "https://example.com/test.mp3"
    assert test_clip.duration == 180
    assert test_clip.tags == "test,dao"
    assert test_clip.play_count == 0
    assert test_clip.id is not None

    # Get the clip by ID
    retrieved_clip = await clip_dao.get_clip_by_id(test_clip.id)

    assert retrieved_clip is not None
    assert retrieved_clip.id == test_clip.id
    assert retrieved_clip.name == test_clip.name
    assert retrieved_clip.description == test_clip.description
    assert retrieved_clip.url == test_clip.url


@pytest.mark.anyio
async def test_update_clip() -> None:
    """Test updating a clip in the database."""
    clip_dao = ClipDAO()

    # Create a test clip
    test_clip = await clip_dao.create_clip(
        name="Update Test",
        description="A clip to test updates",
        url="https://example.com/update.mp3",
        duration=200,
        tags="test,update",
    )

    # Update the clip
    await clip_dao.update_clip(
        test_clip.id,
        name="Updated Name",
        description="Updated description",
    )

    # Get the updated clip
    updated_clip = await clip_dao.get_clip_by_id(test_clip.id)

    assert updated_clip is not None
    assert updated_clip.name == "Updated Name"
    assert updated_clip.description == "Updated description"
    # Other fields should remain unchanged
    assert updated_clip.url == test_clip.url
    assert updated_clip.duration == test_clip.duration
    assert updated_clip.tags == test_clip.tags


@pytest.mark.anyio
async def test_delete_clip() -> None:
    """Test deleting a clip from the database."""
    clip_dao = ClipDAO()

    # Create a test clip
    test_clip = await clip_dao.create_clip(
        name="Delete Test",
        description="A clip to test deletion",
        url="https://example.com/delete.mp3",
        duration=150,
        tags="test,delete",
    )

    # Verify clip exists
    assert await clip_dao.get_clip_by_id(test_clip.id) is not None

    # Delete the clip
    await clip_dao.delete_clip(test_clip.id)

    # Verify clip no longer exists
    assert await clip_dao.get_clip_by_id(test_clip.id) is None


@pytest.mark.anyio
async def test_search_clips() -> None:
    """Test searching for clips in the database."""
    clip_dao = ClipDAO()

    # Create test clips with different tags
    await clip_dao.create_clip(
        name="Jazz Song",
        description="A jazz song",
        url="https://example.com/jazz.mp3",
        duration=180,
        tags="jazz,instrumental",
    )

    await clip_dao.create_clip(
        name="Blues Song",
        description="A blues song",
        url="https://example.com/blues.mp3",
        duration=210,
        tags="blues,guitar",
    )

    # Search by tag
    jazz_results = await clip_dao.search_clips("jazz")
    assert len(jazz_results) >= 1
    assert any(clip.name == "Jazz Song" for clip in jazz_results)
    assert not any(clip.name == "Blues Song" for clip in jazz_results)

    # Search by name
    blues_results = await clip_dao.search_clips("Blues")
    assert len(blues_results) >= 1
    assert any(clip.name == "Blues Song" for clip in blues_results)

    # Search by description
    guitar_results = await clip_dao.search_clips("guitar")
    assert len(guitar_results) >= 1
    assert any(clip.tags == "blues,guitar" for clip in guitar_results)


@pytest.mark.anyio
async def test_increment_play_count() -> None:
    """Test incrementing a clip's play count."""
    clip_dao = ClipDAO()

    # Create a test clip
    test_clip = await clip_dao.create_clip(
        name="Play Count Test",
        description="Testing play count incrementation",
        url="https://example.com/playcount.mp3",
        duration=180,
        tags="test,playcount",
    )

    # Initial play count should be 0
    assert test_clip.play_count == 0

    # Increment play count
    await clip_dao.increment_play_count(test_clip.id)

    # Get updated clip
    updated_clip = await clip_dao.get_clip_by_id(test_clip.id)
    assert updated_clip is not None
    assert updated_clip.play_count == 1

    # Increment again
    await clip_dao.increment_play_count(test_clip.id)

    # Verify play count increased again
    updated_clip = await clip_dao.get_clip_by_id(test_clip.id)
    assert updated_clip is not None
    assert updated_clip.play_count == 2
