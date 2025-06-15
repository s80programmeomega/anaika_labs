from django.urls import path
from .views import EvaluationCreateView

urlpatterns = [
    path(
        "evaluations/",
        EvaluationCreateView.as_view(
            {
                "post": "create",
                "get": "list",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
                "options": "options",
            }
        ),
        name="evaluation-create",
    ),
]
