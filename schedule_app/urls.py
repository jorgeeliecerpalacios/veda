from django.urls import path

# pyrefly: ignore [missing-import]
from . import views  # Crearemos estas vistas sencillas en el paso del front

urlpatterns = [
    # Ejemplo: /schedule/
    path(route="", view=views.SubjectListView.as_view(), name="subject_list"),
    # Ejemplo: /schedule/subject/add/
    path(
        route="subject/add/",
        view=views.SubjectCreateView.as_view(),
        name="subject_create",
    ),
    # path(
    # route='',
    # view=views.index,
    # name='index'
    # ),
]
