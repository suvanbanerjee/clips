from datetime import datetime

from piccolo.columns import Integer, Text, Timestamp, Varchar
from piccolo.table import Table


class ClipModel(Table):
    """Model for storing audio clips and their metadata."""

    name = Varchar(length=200, null=False, help_text="Name of the clip")
    url = Text(null=False, help_text="URL of the audio file")
    description = Text(null=True, help_text="Description of the clip")
    duration = Integer(null=True, help_text="Duration of the clip in seconds")
    play_count = Integer(
        default=0,
        help_text="Number of times the clip has been played",
    )
    tags = Text(null=True, help_text="Comma-separated tags for the clip")
    created_at = Timestamp(default=datetime.now, help_text="When the clip was added")
    updated_at = Timestamp(
        default=datetime.now,
        help_text="When the clip was last updated",
    )
