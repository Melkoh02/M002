from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView

from users.api.v1.viewsets import CustomLoginView

api_v1_patterns = [
    path("", include("users.api.v1.urls")),
    path("authenticate/", CustomLoginView.as_view()),
]

urlpatterns = [
    path("api/v1/", include(api_v1_patterns)),
    path('admin/', admin.site.urls),
    # Swagger
    path("api-docs/schema/", SpectacularJSONAPIView.as_view(), name="schema"),
    path("api-docs/", SpectacularSwaggerView.as_view(url_name='schema'), name="api_docs"),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve the index.html for all other routes in production
if not settings.DEBUG:
    urlpatterns += [re_path(r".*", TemplateView.as_view(template_name='index.html'))]
