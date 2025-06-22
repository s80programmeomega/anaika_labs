from django.forms import ValidationError
import magic


allowed_audio_extensions = [
    "mp3",
    "mpga",
    "mpeg",
    "mpg",
    "mpe",
    "wav",
    "aac",
    "flac",
    "m4a",
]
allowed_mime_types = [
    "audio/mpeg",
    "audio/mp3",
    "audio/mpeg3",
    "audio/wav",
    "audio/wave",
    "audio/x-wav",
    "audio/aac",
    "audio/mp4",
    "audio/flac",
    "audio/x-flac",
]


def validate_file_content_type(file):
    """
    Validate the content type of a file to ensure it is an audio file.

    Args:
        file: The file to validate.

    Raises:
        ValidationError: If the file is not an audio file.
    """
    mime = magic.Magic(mime=True)
    content_type = mime.from_buffer(buf=file.read(1024))
    file.seek(0)  # Reset file pointer after reading

    if content_type not in allowed_mime_types:
        raise ValidationError(
            message=f"Invalid file type: {content_type}. Only audio files are allowed."
        )
