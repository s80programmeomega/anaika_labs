from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from pronunciation_evaluation.views import (
    EvaluationViewSet,
    EvaluationResultViewSet,
    FlowResultViewSet,
    PronunciationResultViewSet,
)
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet


router = DefaultRouter()

router.register(prefix="evaluation", viewset=EvaluationViewSet, basename="evaluation")
router.register(prefix="users", viewset=UserViewSet, basename="users")
router.register(
    prefix="evaluation-results",
    viewset=EvaluationResultViewSet,
    basename="evaluation_results",
)
router.register(
    prefix="flow-results", viewset=FlowResultViewSet, basename="flow_results"
)
router.register(
    prefix="pronunciation-results",
    viewset=PronunciationResultViewSet,
    basename="pronunciation_results",
)

drf_spectacular_urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


api_urlpatterns = router.urls + drf_spectacular_urlpatterns
