from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.api.v1.viewsets import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
# router.register("password", PasswordViewSet, basename="password")
# router.register("user-settings", UserSettingsViewSet, basename="user-settings")

urlpatterns = [
    path("", include(router.urls)),
    # path('redirect/<slug:slug>/', DynamicRedirectView.as_view(), name='dynamic_redirect'),
]
