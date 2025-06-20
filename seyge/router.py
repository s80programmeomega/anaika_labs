from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
import jwt
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import UserViewSet
from pronunciation_evaluation.views import (
    EvaluationResultViewSet,
    EvaluationViewSet,
    FlowResultViewSet,
    PronunciationResultViewSet,
)


class CustomDefaultRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        # Get default API root dictionary from parent
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        # Add custom schema routes
        api_root_dict.update(
            {
                "schema": "schema",  # URL pattern name
                "swagger-ui": "swagger-ui",
                "redoc": "redoc",
                "api-token-auth": "api_token_auth",
                "token_obtain_pair": "token_obtain_pair",
                "token_refresh": "token_refresh",
            }
        )
        return self.APIRootView.as_view(api_root_dict=api_root_dict)


router = CustomDefaultRouter()

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

drf_token_urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token, name="api_token_auth")
]
jwt_urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

api_urlpatterns = (
    router.urls + drf_spectacular_urlpatterns + drf_token_urlpatterns + jwt_urlpatterns
)
