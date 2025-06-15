from django.db import models
from django.contrib.auth import get_user_model
from django.http import HttpRequest

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

    def get_user_email(instance, filename):
        return f"{instance.user.email}/{filename}"

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
        return f"{self.user.username} - {self.user.email}"
