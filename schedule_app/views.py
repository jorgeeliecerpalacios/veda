from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Subject


class SubjectListView(ListView):
    """
    Vista principal del Dashboard del Docente.
    Lista todas las materias (Subjects) configuradas en Veda.
    """

    model = Subject
    template_name = "schedule/subject_list.html"
    context_object_name = "subjects"

    def get_context_data(self, **kwargs):  # noqa: ANN003, ANN201
        context = super().get_context_data(**kwargs)
        # Añadimos métricas rápidas para mostrar en tarjetas superiores en el frontend
        context["total_subjects"] = self.get_queryset().count()
        return context


class SubjectCreateView(CreateView):
    """
    Permite al docente registrar una nueva materia, definiendo el país,
    la edad del niño y el grado escolar para alimentar el contexto de la IA.
    """

    model = Subject
    fields = ["name", "description", "country", "target_age", "school_grade"]
    template_name = "schedule/subject_form.html"
    success_url = reverse_lazy("schedule:subject_list")

    def form_valid(self, form):  # noqa: ANN201
        # Aquí, si usas el sistema de autenticación de Django en el futuro,
        # asociamos automáticamente al docente logueado:
        # form.instance.teacher = self.request.user
        return super().form_valid(form)
