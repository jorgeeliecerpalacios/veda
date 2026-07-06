from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
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
        return redirect("ai_core:research_topic", subject_id=block.subject_id)

    return render(request, "resources/add_resource_modal.html", {"block": block})

class ClassBlockDetailView(View):
    def get(self, request, block_id):  # noqa: ANN001, ANN201
        # 1. Buscamos el bloque en la tabla correcta (como el registro 12 que vimos)
        block = get_object_or_404(ClassBlock, id=block_id)

        # 2. Renderizamos directamente la plantilla del Workspace pasando el contexto esperado
        return render(request, "ai_core/lesson_workspace.html", {
            "new_block": block,  # Tu HTML ya usa 'new_block' gracias al ajuste anterior
            "subject": block.subject,
            # Si guardaste datos específicos de la IA como un diccionario en tu base de datos o modelo, 
            # puedes pasarlo aquí. Por ejemplo:
            # "ai_data": block.get_ai_data_json() o lo que requiera tu interfaz
        })
