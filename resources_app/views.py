import json

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
        return redirect("resources:lesson_workspace_detail", block_id=block.id)

    return render(request, "resources/add_resource_modal.html", {"block": block})

class ClassBlockDetailView(View):
    def get(self, request, block_id):  # noqa: ANN001, ANN201
        block = get_object_or_404(ClassBlock, id=block_id)

        ai_data = {}
        lesson_material = ""

        if block.ai_generated_content:
            try:
                raw_json = json.loads(block.ai_generated_content)

                # Accedemos de forma segura al objeto interno de la IA
                adaptation = raw_json.get("pedagogical_adaptation", {})

                # 🎯 MAPEO EXACTO BASADO EN TU CAPTURA
                ai_data = {
                    "suggested_activity": " / ".join(adaptation.get("scaffolding_strategies", [])) or "No activity specified",
                    "key_learning_points": adaptation.get("learning_objectives", []),
                    "multimedia_guidelines": {
                        "visuals": "Search graphs or numerical lines for irrational numbers.",
                        "videos": "Search visual proofs of the Pythagorean theorem."
                    }
                }

                # Creamos un material de lectura estructurado y estético en vez de tirar el JSON crudo
                lesson_material = f"Definition:\n{adaptation.get('definition', '')}\n\n"
                lesson_material += "Key Concepts:\n" + "\n".join([f"• {c}" for c in adaptation.get("key_concepts", [])])

            except json.JSONDecodeError:
                lesson_material = block.ai_generated_content

        return render(request, "ai_core/lesson_workspace.html", {
            "block": block,              # 👈 IMPORTANTE: Usamos 'block' para que coincida con tu HTML
            "new_block": block,          # Mantenemos este por el modal y los recursos
            "subject": block.subject,
            "ai_data": ai_data,
            "lesson_material": lesson_material, # 👈 Variable limpia con el texto de la clase
        })
