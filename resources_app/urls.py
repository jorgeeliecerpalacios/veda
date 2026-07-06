from django.urls import path

# pyrefly: ignore [missing-import]
from . import views

app_name = "resources"

urlpatterns = [
    path(route="add/<int:block_id>/", view=views.add_resource, name="add_resource"),
]
