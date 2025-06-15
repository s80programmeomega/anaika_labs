from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .models import Evaluation
from .serializers import EvaluationSerializer


class EvaluationCreateView(ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     # serializer.save(user=self.request.user)
