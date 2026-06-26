from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [
    path(route="add/<int:block_id>/", views=views.add_resource, name="add_resource"),
]
