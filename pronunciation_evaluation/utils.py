import os
import wave

import pyaudio
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from pydub import AudioSegment


def generate_id():
    """
    Generates a unique identifier for audio files

    Returns:
    str: Unique identifier
    """
    import uuid

    return str(uuid.uuid4().hex[:8])  # Shorten to 8 characters for simplicity


def upload_path(instance):
    return f"{instance.user.email}/"


# ========================
# Audio Recording Module
# ========================
def record_audio(user, duration: int = 5) -> None:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # Sample rate compatible with Whisper

    media_path = os.path.join(settings.MEDIA_ROOT, "user_audio", user.email)

    now = timezone.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    filename = os.path.join(media_path, f"{timestamp}.wav")

    os.makedirs(media_path, exist_ok=True)

    p = pyaudio.PyAudio()

    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        frames = []
        print(f"Recording {duration} seconds...")

        # Capture audio in chunks to prevent buffer overflow
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        # Save raw audio data
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    print(f"Recording saved to {filename}")
    convert_audio(
        input_path=filename,
        output_format="mp3",
    )


def convert_audio(input_path, output_format="mp3", bitrate=None, mpeg_layer=None):
    output_path = str(input_path).replace("wav", output_format)
    # Load input file
    audio = AudioSegment.from_file(input_path)

    # Prepare export parameters
    params = {"format": output_format}

    if bitrate:
        params["bitrate"] = bitrate

    # Handle MPEG layer specification
    if output_format in ["mp1", "mp2", "mp3"] and mpeg_layer:
        params["codec"] = f"mp{mpeg_layer}"

    # Special handling for MPEG formats
    if output_format == "mpeg" or output_format == "mpg":
        params["format"] = "mp3"  # Default to MP3 for .mpeg/.mpg containers
        if not output_path.endswith((".mpeg", ".mpg")):
            output_path += ".mpeg"

    # Export the file
    audio.export(output_path, **params)
    return output_path
