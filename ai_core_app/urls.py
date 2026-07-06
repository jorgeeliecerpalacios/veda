from django.urls import path

# pyrefly: ignore [missing-import]
from .views import ResearchTopicView

urlpatterns = [
    # Ejemplo: /ai-core/research/5/ (Investigar un tema para la materia con ID 5)
    path(
        route="research/<int:subject_id>/",
        view=ResearchTopicView.as_view(),
        name="research_topic",
    ),
]
