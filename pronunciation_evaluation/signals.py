from django.db.models.signals import post_save
from django.dispatch import receiver

from pronunciation_evaluation import utils
from .models import Evaluation, FlowResult, PronunciationResult, EvaluationResult


@receiver(signal=post_save, sender=Evaluation)
def create_result_for_evaluation(sender, instance: Evaluation, created, **kwargs):
    if created:
        # Populate Result fields as needed, example:
        evaluation_results = utils.evaluate_pronunciation(
            user_audio_path=instance.user_audio.path,
            target_audio_path=instance.reference_audio.path,
            base_text=instance.reference_text,
        )

        # user clarity
        user_clarity_result = evaluation_results["clarity"]

        # //////////////////////////////////////////////////////////

        # user flow results
        fr = evaluation_results["flow"]
        user_flow_results = FlowResult.objects.create(
            evaluation=instance,
            speaking_ratio=fr["speaking_ratio"],
            speaking_speed=fr["speaking_speed"],
            flow_score=fr["score"],
        )
        # //////////////////////////////////////////////////////////

        # user pronunciationresults
        pr = evaluation_results["pronunciation"]
        user_pronunciation_results = PronunciationResult.objects.create(
            evaluation=instance,
            score=pr["score"],
            percentage=pr["percentage"],
            user_phonemes=pr["user_phonemes"],
            reference_phonemes=pr["reference_phonemes"],
        )
        # //////////////////////////////////////////////////////////

        # Reference flow results
        rf_ratio, rf_speed, rf_score = utils.evaluate_flow(
            audio_path=instance.reference_audio.path
        )

        target_flow_results = FlowResult.objects.create(
            evaluation=instance,
            speaking_ratio=rf_ratio,
            speaking_speed=rf_speed,
            flow_score=rf_score,
        )
        # /////////////////////////////////////////////////////////

        evaluation_result = EvaluationResult.objects.create(
            clarity_score=user_clarity_result,
            reference_flow_result=target_flow_results,
            user_flow_result=user_flow_results,
            pronunciation_result=user_pronunciation_results,
        )
        instance.result = evaluation_result # type: ignore
        instance.save(update_fields=["result"])
