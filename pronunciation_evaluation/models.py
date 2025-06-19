from django.db import models
from django.contrib.auth import get_user_model

from pronunciation_evaluation.utils import generate_id


class Evaluation(models.Model):
    id = models.CharField(primary_key=True, default=generate_id, editable=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="evaluations"
    )

    reference_text = models.TextField(
        help_text="The reference text for the pronunciation evaluation.",
        default="",
    )

    def get_user_email(instance, filename) -> str:  # type: ignore
        return f"evaluations/{filename}"

    reference_audio = models.FileField(
        upload_to=get_user_email,
        help_text="Audio file of the reference text for pronunciation evaluation.",
        blank=True,
        null=True,
    )

    user_audio = models.FileField(
        upload_to=get_user_email,
        help_text="Audio file of the user's pronunciation attempt.",
        blank=True,
        null=True,
    )

    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.user.username} - {self.user.email}"


class FlowResult(models.Model):
    id = models.CharField(primary_key=True, default=generate_id, editable=False)

    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.CASCADE, related_name="flow_results"
    )

    speaking_ratio = models.FloatField(
        help_text="The ratio of speaking time to total time in the audio recording."
    )
    speaking_speed = models.FloatField(
        help_text="The speaking speed in words per minute."
    )

    flow_score = models.FloatField(
        help_text="The overall flow score based on speaking speed and continuity."
    )

    date_added = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f"Flow Result - Speaking Ratio: {self.speaking_ratio}, Speed: {self.speaking_speed} WPM, Score: {self.flow_score}%"

    def __str__(self) -> str:
        return self.id


class PronunciationResult(models.Model):
    id = models.CharField(primary_key=True, default=generate_id, editable=False)

    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.CASCADE, related_name="pronunciation_results"
    )

    score = models.FloatField(
        help_text="The pronunciation score based on phonetic analysis."
    )
    percentage = models.FloatField(
        help_text="The percentage of correct pronunciation compared to the reference."
    )
    user_phonemes = models.CharField(
        help_text="The phonemes detected in the user's pronunciation."
    )
    reference_phonemes = models.CharField(
        help_text="The phonemes present in the reference pronunciation."
    )

    date_added = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f"Pronunciation Result - Score: {self.score}, Percentage: {self.percentage}%"

    def __str__(self) -> str:
        return self.id


class EvaluationResult(models.Model):
    id = models.CharField(primary_key=True, default=generate_id, editable=False)
    evaluation = models.OneToOneField(
        Evaluation, on_delete=models.CASCADE, related_name="result"
    )
    clarity_score = models.FloatField(
        help_text="The clarity score of the user's pronunciation."
    )
    reference_flow_result = models.OneToOneField(
        FlowResult,
        on_delete=models.SET_NULL,
        related_name="reference_result",
        null=True,
        blank=True,
    )
    user_flow_result = models.OneToOneField(
        FlowResult,
        on_delete=models.SET_NULL,
        related_name="user_result",
        null=True,
        blank=True,
    )
    pronunciation_result = models.OneToOneField(
        PronunciationResult,
        on_delete=models.SET_NULL,
        related_name="result",
        null=True,
        blank=True,
    )

    date_added = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return (
            f"Result for Evaluation {self.evaluation.id},\n"
            f"User: {self.evaluation.user.email},\n"
            f"Clarity Score: {self.clarity_score},\n"
            f"Reference Flow Result: {self.reference_flow_result},\n"
            f"User Flow Result: {self.user_flow_result},\n"
            f"Pronunciation Result: {self.pronunciation_result}\n"
        )

    def __str__(self) -> str:
        return self.id
