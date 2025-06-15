from django.http import HttpRequest
from .models import Evaluation
from rest_framework import serializers


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = "__all__"
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        evaluation = Evaluation.objects.create(**validated_data)
        return evaluation
