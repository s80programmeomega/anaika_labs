import os
import wave

import librosa
import numpy as np
import pyaudio
import whisper
from Bio.Align import PairwiseAligner
from django.conf import settings
from django.utils import timezone
from Levenshtein import ratio as levenshtein_ratio
from phonemizer import phonemize
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


# ========================
# Speech Processing Module
# ========================


def transcribe_audio(file_path: str) -> str:
    """
    Converts speech to text using OpenAI's Whisper

    Args:
    file_path (str): Path to audio file

    Returns:
    str: Transcribed text (lowercase, no punctuation)

    Reference: Radford et al. (2022) Robust Speech Recognition
    via Large-Scale Weak Supervision
    """
    model = whisper.load_model(name="small")
    result = model.transcribe(audio=file_path, verbose=True, language="fr")
    print(f"===> Detected Language: {result['language']} <====")
    return str(result["text"]).strip()


# ========================
# Evaluation Metrics
# ========================


def evaluate_clarity(reference: str, transcription: str) -> float:
    """
    Calculates clarity score using Levenshtein ratio

    Args:
    reference (str): Expected text
    transcription (str): User's spoken text

    Returns:
    float: Similarity score between 0-1

    Reference: Levenshtein, V. (1966) Binary codes capable of
    correcting deletions, insertions, and reversals
    """
    return levenshtein_ratio(s1=reference.lower(), s2=transcription.lower())


def evaluate_flow(audio_path: str) -> tuple:
    """
    Analyzes speech fluency through:
    1. Speaking rate (words per minute)
    2. Pause frequency
    3. Speech continuity

    Args:
    audio_path (str): Path to audio file

    Returns:
    float: Fluency score between 0-1
    """
    y, sr = librosa.load(path=audio_path, sr=16000)

    # Voice activity detection
    intervals = librosa.effects.split(y=y, top_db=25)

    # Calculate speech duration
    speech_samples = sum(end - start for start, end in intervals)
    total_duration = len(y) / sr
    speaking_ratio = speech_samples / len(y)
    speaking_ratio = round(number=speaking_ratio*100, ndigits=2)

    # Words per minute calculation
    transcription = transcribe_audio(audio_path)
    words = len(transcription.split())
    speed = words / (total_duration / 60)
    speed = int(round(number=speed, ndigits=0))

    # Ideal rate: 120 WPM (adjust for French)
    rate_score = np.exp(-0.5 * ((speed - 100) / 40) ** 2)
    continuity_score = 1 - (len(intervals) / 20)  # Fewer pauses better

    flow_score = 0.6 * rate_score + 0.4 * continuity_score
    flow_score = round(number=flow_score*100, ndigits=2)

    return speaking_ratio, speed, flow_score


def evaluate_pronunciation(user_audio_path: str, target_audio_path: str, base_text: str):
    """
    Evaluates a user's pronunciation by comparing their spoken audio to a target reference audio and base text.

    This function performs the following steps:
    1. Transcribes both the user's audio and the target audio to text.
    2. Converts the base text and the user's transcription to phonemes.
    3. Aligns the user's phonemes with the reference phonemes and computes a pronunciation score.
    4. Evaluates the clarity of the user's transcription compared to the base text.
    5. Assesses the flow of the user's speech (e.g., speaking ratio, speed, and flow score).

    Args:
        user_audio_path (str): Path to the user's audio file.
        target_audio_path (str): Path to the target/reference audio file.
        base_text (str): The reference text that the user is expected to pronounce.

    Returns:
        dict: A dictionary containing:
            - "clarity": Clarity score as a percentage.
            - "flow": Dictionary with "speaking_ratio", "speaking_speed", and "score" (percentage).
            - "pronunciation": Dictionary with "score" (identity count), "percentage" (normalized score), 
              "user_phonemes", and "reference_phonemes".

    Raises:
        Any exceptions raised by the underlying transcription, phonemization, or evaluation functions.
    """


    result = {}

    user_text = transcribe_audio(user_audio_path)
    target_text = transcribe_audio(target_audio_path)

    print(f"{user_text=}")
    print(f"{target_text=}")

    base_phonemes = phonemize(text=base_text, language="fr-fr")

    audio1_phonemes = phonemize(
        text=user_text,
        language="fr-fr",
    )

    aligner = PairwiseAligner()
    user_alignments = aligner.align(audio1_phonemes, base_phonemes)

    user_alignment = user_alignments[0]

    print(f"{user_alignments=}")

    user_count = user_alignment.counts()
    user_score = user_count.identities

    user_max_len = max(len(audio1_phonemes), len(base_phonemes))

    user_normalized_score = user_score / user_max_len if user_max_len > 0 else 0
    percentage = user_normalized_score * 100
    percentage = round(number=percentage, ndigits=2)

    print("///////////////////////////////")
    print("Pronunciations Evaluation:")
    print(f"User pronunciation score: {user_score}, Percentage: {percentage}%")
    print("///////////////////////////////")

    clarity_score = evaluate_clarity(
        reference=base_text, transcription=user_text)
    clarity_score = round(number=clarity_score*100, ndigits=2)

    print("///////////////////////////////")
    print("Clarity Evaluation:")
    print(
        f"User clarity score: {clarity_score}%"
    )

    print("///////////////////////////////")

    flow = evaluate_flow(audio_path=user_audio_path)

    print("///////////////////////////////")
    print("Flow Evaluation:")
    print(f"User flow score: {flow[2]}%")
    print("///////////////////////////////")

    result["clarity"] = clarity_score
    result["flow"] = {
        "speaking_ratio": flow[0],
        "speaking_speed": flow[1],
        "score": flow[2],

    }
    result["pronunciation"] = {
        "score": user_score,
        "percentage": percentage,
        "user_phonemes": audio1_phonemes,
        "reference_phonemes": base_phonemes,
    }
    return result
