"""User model."""

# Django
# Utilities
# pyrefly: ignore [missing-import]
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User model.
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")

    TYPE_IDENTIFICATION_CHOICES = (
        ("PP", "Pasaporte"),
        ("Id", "Documento de identidad"),
    )

    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profile_images/photo",
        blank=True,
        null=True,
        verbose_name=_("Imagen de perfil"),
    )
    type_identification = models.CharField(
        max_length=10,
        choices=TYPE_IDENTIFICATION_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Tipo de identificacion"),
    )
    number_identification = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text=_("Numero identificacion"),
        verbose_name=_("Numero de identificacion"),
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text=_("Numero telefonico"),
        verbose_name=_("Numero telefonico"),
    )
    address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=("Direccion"),
        verbose_name=_("Direccion"),
    )

    is_teacher = models.BooleanField(
        "Es docente",
        default=False,
        help_text=(
            "Indica si el usuario es un docente. Si es verdadero, el usuario tendrá acceso a funcionalidades específicas para docentes."
        ),
    )

    is_student = models.BooleanField(
        "Es estudiante",
        default=False,
        help_text=(
            "Indica si el usuario es un estudiante. Si es verdadero, el usuario tendrá acceso a funcionalidades específicas para estudiantes."
        ),
    )

    def __str__(self) -> str:
        return self.username

    def get_short_name(self):  # noqa: ANN201
        return self.username
