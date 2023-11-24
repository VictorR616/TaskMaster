from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El campo de correo electrónico es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=25,
        verbose_name="Correo Electrónico",
        help_text="Ingrese su dirección de correo electrónico.",
    )
    password1 = models.CharField(
        max_length=128,
        verbose_name="Contraseña",
        help_text="Ingrese su contraseña.",
    )
    password2 = models.CharField(
        max_length=128,
        verbose_name="Confirmar Contraseña",
        help_text="Ingrese nuevamente su contraseña para confirmar.",
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Nombre",
        help_text="Ingrese su nombre.",
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Apellido",
        help_text="Ingrese su apellido.",
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Registro",
        help_text="Fecha y hora en que el usuario se registró.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la cuenta del usuario está activa.",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Personal de Staff",
        help_text="Indica si el usuario tiene acceso al panel de administración.",
    )

    profile_picture = models.ImageField(
        upload_to="users/profile_pictures/",
        default="users/profile_pictures/default.png",
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email
