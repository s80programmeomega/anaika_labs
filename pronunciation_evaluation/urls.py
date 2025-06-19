from django.urls import path
from .views import EvaluationViewSet

urlpatterns = [
    path(
        "evaluations/",
        EvaluationViewSet.as_view(
            {'get': 'list'}),
        name="evaluation",
    ),
]
