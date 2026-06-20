from django.db import models


class Subject(models.Model):
    """
    Representa una materia o asignatura dictada por el docente.
    """

    # Relacionamos con el usuario de Django por si en el futuro manejas login de maestros
    teacher = models.ForeignKey(
        "users_app.User",
        on_delete=models.CASCADE,
        related_name="subjects",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50, default="Colombia")
    target_age = models.PositiveIntegerField(
        help_text="Edad promedio de los niños para ajustar la IA"
    )
    school_grade = models.CharField(
        max_length=50, help_text="Ej: 3rd Grade, Primaria, etc."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.school_grade} ({self.country})"


class ClassBlock(models.Model):
    """
    Cada bloque de tiempo o sesión en el calendario asociado a una materia.
    """

    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="class_blocks"
    )
    topic_title = models.CharField(
        max_length=200, help_text="Tema de la clase generado o editado"
    )
    ai_generated_content = models.TextField(
        blank=True, null=True, help_text="El desglose de puntos clave de la IA"
    )
    pedagogical_methodology = models.CharField(max_length=100, default="Constructivism")

    # Campos de calendario
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Control del docente
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.topic_title} ({self.subject.name})"
