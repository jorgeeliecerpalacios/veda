from django.db import models

class ClassBlock(models.Model):
    # Campos que ya venías usando en tus formularios y respuestas
    topic_title = models.CharField(max_length=250)
    pedagogical_methodology = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # El contenido JSON o texto completo que te genera la IA
    ai_generated_content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.topic_title} ({self.pedagogical_methodology})"
