from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView  # 👈 Añadimos CreateView aquí

# pyrefly: ignore [missing-import]
from .models import ClassBlock, Subject


class SubjectListView(ListView):
    """
    Vista principal del calendario / agenda del docente.
    Muestra los bloques de clase ordenados cronológicamente.
    """
    model = ClassBlock
    template_name = "schedule/calendar_dashboard.html"
    context_object_name = "class_blocks"

    def get_queryset(self):  # noqa: ANN201
        # Retornamos los bloques ordenados por fecha de inicio, 
        # trayendo de golpe la materia (select_related) para optimizar consultas a la DB
        return ClassBlock.objects.select_related('subject').order_by('start_time')

    def get_context_data(self, **kwargs):  # noqa: ANN003, ANN201
        context = super().get_context_data(**kwargs)
        # También pasamos las materias disponibles por si necesitas filtros en el front
        context["subjects"] = Subject.objects.all()
        return context


# ➕ NUEVA VISTA: Añadimos la vista que le hace falta a tus URLs
class SubjectCreateView(CreateView):
    """
    Vista para que el docente pueda añadir una nueva materia (Subject).
    """
    model = Subject
    fields = ["name", "description", "country", "target_age", "school_grade"]  # Los campos correspondientes de tu modelo Subject
    template_name = "schedule/subject_form.html"
    success_url = reverse_lazy("schedule:my_subjects_list")  # Al guardar, regresa a la agenda

class SubjectDashboardListView(ListView):
    """
    Vista global para listar todas las materias (My Subjects) 
    con acceso directo a sus configuraciones o detalles.
    """
    model = Subject
    template_name = "schedule/subject_dashboard.html"
    context_object_name = "subjects"

    def get_queryset(self):  # noqa: ANN201
        return Subject.objects.all().order_by('name')
