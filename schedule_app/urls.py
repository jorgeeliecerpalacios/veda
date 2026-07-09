from django.urls import path

# pyrefly: ignore [missing-import]
from . import views

app_name = "schedule"  # Namespace para reversar URLs limpiamente

urlpatterns = [
    # /schedule/ -> Panel del Calendario
    path(route="", view=views.SubjectListView.as_view(), name="subject_list"),

    # /schedule/subject/add/ -> Crear materia
    path(
        route="subject/add/",
        view=views.SubjectCreateView.as_view(),
        name="subject_create",
    ),
    # 🎯 NUEVA: Ruta para listar las materias de forma independiente
    path(route="subjects/all/", view=views.SubjectDashboardListView.as_view(), name="my_subjects_list"),
]
