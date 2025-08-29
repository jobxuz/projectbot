from django.contrib.auth.forms import AuthenticationForm
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

class LoginForm(AuthenticationForm):
    def clean(self):
        return super().clean()


admin.site.login_form = LoginForm
admin.site.login_template = "login.html"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include("apps.application.urls")),
    path('bot/', include("apps.bot.urls")),

    path("i18n/", include("django.conf.urls.i18n")),

    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    path("redocs/", SpectacularRedocView.as_view(url_name="api-schema"), name="api-redocs"),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)