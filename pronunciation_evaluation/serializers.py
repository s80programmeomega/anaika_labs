from .models import Evaluation, EvaluationResult, FlowResult, PronunciationResult
from rest_framework import serializers
from accounts.serializers import UserSerializer


class EvaluationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    result = "EvaluationResultSerializer"

    class Meta:
        model = Evaluation
        fields = "__all__"
        read_only_fields: list[str] = ["user"]

    def create(self, validated_data) -> Evaluation:
        evaluation: Evaluation = Evaluation.objects.create(**validated_data)
        return evaluation


class FlowResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowResult
        fields = "__all__"

    def create(self, validated_data) -> FlowResult:
        flow_result: FlowResult = FlowResult.objects.create(**validated_data)
        return flow_result


class PronunciationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PronunciationResult
        fields = "__all__"

    def create(self, validated_data) -> PronunciationResult:
        pronunciation_result: PronunciationResult = PronunciationResult.objects.create(
            **validated_data
        )
        return pronunciation_result


class EvaluationResultSerializer(serializers.ModelSerializer):
    evaluation = EvaluationSerializer(read_only=True)
    reference_flow_result = FlowResultSerializer(
        read_only=True, help_text="Reference flow result for the evaluation."
    )
    user_flow_result = FlowResultSerializer(
        read_only=True, help_text="User flow result for the evaluation."
    )
    pronunciation_result = PronunciationResultSerializer(
        read_only=True, help_text="Pronunciation result for the evaluation."
    )

    class Meta:
        model = EvaluationResult
        fields = "__all__"
        read_only_fields: list[str] = [
            "evaluation",
            "reference_flow_result",
            "user_flow_result",
            "pronunciation_result",
        ]

    def create(self, validated_data) -> EvaluationResult:
        user_result: EvaluationResult = EvaluationResult.objects.create(
            **validated_data
        )
        return user_result
