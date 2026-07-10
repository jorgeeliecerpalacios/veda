from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware
from django.views.generic import (  # 👈 Añadimos CreateView y View aquí
    CreateView,
    ListView,
    View,
)

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

class EditBlockScheduleView(View):
    def post(self, request, block_id):  # noqa: ANN001, ANN201
        block = get_object_or_404(ClassBlock, id=block_id)

        # Capturamos los nuevos inputs de tiempo
        start_str = request.POST.get("start_time")
        end_str = request.POST.get("end_time")

        # Procesamos start_time
        if start_str:
            start_dt = parse_datetime(start_str)
            if start_dt and is_naive(start_dt):
                start_dt = make_aware(start_dt)
            block.start_time = start_dt

        # Procesamos end_time
        if end_str:
            end_dt = parse_datetime(end_str)
            if end_dt and is_naive(end_dt):
                end_dt = make_aware(end_dt)
            block.end_time = end_dt

        block.save()
        messages.success(request, "¡Horario de la clase actualizado con éxito!")

        # Redireccionamos de vuelta al mismo workspace detallado
        return redirect("resources:lesson_workspace_detail", block_id=block.id)
