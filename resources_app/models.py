from django.db import models


class TrackableResource(models.Model):
    """
    Recursos multimedia (Imágenes, Videos, Audios) asociados a un bloque de clase específico.
    """

    RESOURCE_TYPES = [
        ("IMAGE", "Image / Infographic"),
        ("VIDEO", "Video Link or File"),
        ("AUDIO", "Audio / Podcast Lesson"),
        ("DOC", "Exam / Worksheet Document"),
    ]

    class_block = models.ForeignKey(
        "schedule_app.ClassBlock", on_delete=models.CASCADE, related_name='trackable_resources'
    )
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    title = models.CharField(max_length=150)

    # Permite subir el archivo localmente o guardar una URL externa (ej. un video de YouTube)
    file_attachment = models.FileField(
        upload_to="veda_resources/", blank=True, null=True
    )
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="Enlace a video de YouTube, audio externo, etc.",
    )

    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.get_resource_type_display()}] {self.title}"

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('document', 'PDF / Documento'),
        ('video', 'YouTube / Video'),
        ('link', 'Enlace Web'),
    )

    class_block = models.ForeignKey("schedule_app.ClassBlock", on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='class_resources/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.get_resource_type_display()}] {self.title}"