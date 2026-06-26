from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ai_core_app.models import ClassBlock

from .models import Resource


def add_resource(request, block_id):  # noqa: ANN001, ANN201
    block = get_object_or_404(ClassBlock, id=block_id)

    if request.method == "POST":
        title = request.POST.get("title")
        resource_type = request.POST.get("resource_type")
        url = request.POST.get("url")
        file = request.FILES.get("file")  # ¡Capturamos el archivo físico!

        # Guardamos en la base de datos
        Resource.objects.create(
            class_block=block,
            title=title,
            resource_type=resource_type,
            url=url,
            file=file,
        )

        messages.success(request, f"¡Recurso '{title}' adjuntado con éxito!")
        # Redirigimos de vuelta al workspace de esa clase (ajusta el nombre de tu ruta si es distinto)
        return redirect("ai_core:lesson_workspace", block_id=block.id)

    return render(request, "resources/add_resource_modal.html", {"block": block})
