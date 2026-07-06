"""
URL configuration for veda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    # Enrutadores modulares de Veda
    path("schedule/", include(("schedule_app.urls", "schedule"), namespace="schedule")),
    path("ai-core/", include(("ai_core_app.urls", "ai_core"), namespace="ai_core")),
    path("resources/", include(("resources_app.urls", "resources"), namespace="resources")),
]

# Servir archivos multimedia (imágenes, audios, videos) en entorno de desarrollo local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
