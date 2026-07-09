import json

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from schedule_app.models import ClassBlock

# pyrefly: ignore [missing-import]
from .models import Resource


def add_resource(request, block_id):  # noqa: ANN001, ANN201
    block = get_object_or_404(ClassBlock, id=block_id)

    if request.method == "POST":
        title = request.POST.get("title")
        resource_type = request.POST.get("resource_type")
        url = request.POST.get("url")
        file = request.FILES.get("file")

        # Guardamos en la base de datos de forma limpia
        Resource.objects.create(
            class_block=block,
            title=title,
            resource_type=resource_type,
            url=url if resource_type != 'document' else None, # Limpieza opcional por seguridad
            file=file if resource_type == 'document' else None,
        )

        messages.success(request, f"¡Recurso '{title}' adjuntado con éxito!")

        # 🛠️ AJUSTE AQUÍ: Cambiamos 'block_id=block.id' por el argumento que tu ruta 'research' espera.
        # Basado en tus URLs anteriores, lo más probable es que use 'pk' o 'subject_id' (en tus logs salía /research/1/)
        return redirect("resources:lesson_workspace_detail", block_id=block.id)

    return render(request, "resources/add_resource_modal.html", {"block": block})

class ClassBlockDetailView(View):
    def get(self, request, block_id):  # noqa: ANN001, ANN201
        block = get_object_or_404(ClassBlock, id=block_id)

        ai_data = {}
        lesson_material = ""

        if block.ai_generated_content:
            try:
                # Cargamos el JSON estructurado inmutable desde la base de datos
                raw_json = json.loads(block.ai_generated_content)

                # 🎯 MAPEO DIRECTO Y LIMPIO DESDE NUESTRO NUEVO SCHEMA DE PYDANTIC
                multimedia = raw_json.get("multimedia_guidelines", {})

                ai_data = {
                    "suggested_activity": raw_json.get("suggested_activity", "No activity specified"),
                    "key_learning_points": raw_json.get("key_learning_points", []),
                    "multimedia_guidelines": {
                        "visuals": multimedia.get("visuals", f"infografia de {block.topic_title}"),
                        "videos": multimedia.get("videos", f"video de {block.topic_title}")
                    }
                }

                # Extraemos el material de clase completo que guardó Gemini
                lesson_material = raw_json.get("lesson_material", f"Topic Overview: {block.topic_title}")

            except json.JSONDecodeError:
                lesson_material = block.ai_generated_content

        return render(request, "ai_core/lesson_workspace.html", {
            "block": block,              # Mantenemos consistencia con tu HTML
            "new_block": block,          # Para el modal y el listado de recursos
            "subject": block.subject,
            "ai_data": ai_data,
            "lesson_material": lesson_material,
        })

class MultimediaResourcesListView(ListView):
    """
    Vista global para listar, buscar y filtrar todos los recursos
    multimedia subidos por el docente en la plataforma.
    """
    model = Resource
    template_name = "resources/multimedia_dashboard.html"
    context_object_name = "resources"

    def get_queryset(self):  # noqa: ANN201
        # Empezamos trayendo todos los recursos ordenados por los más recientes
        queryset = Resource.objects.all().order_by('-id')

        # Capturamos los filtros del frontend (barra de búsqueda y tipo)
        search_query = self.request.GET.get('search', '')
        resource_type = self.request.GET.get('type', '')

        if search_query:
            # Filtramos por título del recurso o por el tema de la clase asociada
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(class_block__topic_title__icontains=search_query)
            )

        if resource_type and resource_type != 'all':
            # Filtramos por tipo: 'document', 'video', 'link'
            queryset = queryset.filter(resource_type=resource_type)

        return queryset

    def get_context_data(self, **kwargs):  # noqa: ANN003, ANN201
        context = super().get_context_data(**kwargs)
        # Devolvemos los valores actuales de los filtros para mantenerlos en los inputs del HTML
        context['search_query'] = self.request.GET.get('search', '')
        context['current_type'] = self.request.GET.get('type', 'all')
        return context
