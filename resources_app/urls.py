from django.urls import path

# pyrefly: ignore [missing-import]
from .views import ClassBlockDetailView, add_resource

app_name = "resources"

urlpatterns = [
    path(route="add/<int:block_id>/", view=add_resource, name="add_resource"),

    # 📄 NUEVA RUTA: Para ver directamente un Workspace guardado (Ej: /ai-core/workspace/12/)
    path(
        route="workspace/<int:block_id>/",
        view=ClassBlockDetailView.as_view(),
        name="lesson_workspace_detail",
    ),
]
