from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .models import Evaluation, EvaluationResult, FlowResult, PronunciationResult
from .serializers import FlowResultSerializer, PronunciationResultSerializer
from .serializers import EvaluationSerializer, EvaluationResultSerializer
from . import utils
from rest_framework.response import Response
from rest_framework import status


class EvaluationViewSet(ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save the Evaluation instance, setting user to the authenticated user
        serializer.save(user=request.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class EvaluationResultViewSet(ModelViewSet):
    serializer_class = EvaluationResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            # If the user is a superuser, return all evaluation results
            return EvaluationResult.objects.all()
        # Otherwise, filter results by the authenticated user
        return EvaluationResult.objects.filter(evaluation__user=self.request.user)


class FlowResultViewSet(ModelViewSet):
    queryset = FlowResult.objects.all()
    serializer_class = FlowResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]


class PronunciationResultViewSet(ModelViewSet):
    queryset = PronunciationResult.objects.all()
    serializer_class = PronunciationResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]
