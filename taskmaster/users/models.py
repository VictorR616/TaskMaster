from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Definimos un administrador personalizado para nuestro modelo de usuario
class CustomUserManager(BaseUserManager):
    # Método para crear un usuario estándar
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El campo de correo electrónico es obligatorio")
        email = self.normalize_email(email)  # Normalizamos el correo electrónico
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Configuramos la contraseña
        user.save(using=self._db)
        return user

    # Método para crear un superusuario
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Definimos nuestro modelo de usuario personalizado
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Campo de correo electrónico único
    first_name = models.CharField(max_length=30, blank=True)  # Campo de nombre
    last_name = models.CharField(max_length=30, blank=True)  # Campo de apellido
    date_joined = models.DateTimeField(default=timezone.now)  # Campo de fecha de registro
    is_active = models.BooleanField(default=True)  # Indica si el usuario está activo
    is_staff = models.BooleanField(default=False)  # Indica si el usuario es miembro del staff

    # Ejemplo de campo personalizado: foto de perfil
    profile_picture = models.ImageField(upload_to='users/images/profile_pictures/', blank=True, null=True)
    # Puedes agregar más campos personalizados según tus necesidades

    objects = CustomUserManager()  # Instanciamos nuestro administrador personalizado

    USERNAME_FIELD = "email"  # Campo que se usará como nombre de usuario (correo electrónico)
    REQUIRED_FIELDS = []  # Campos adicionales requeridos al crear un superusuario

    def __str__(self):
        return self.email  # Representación en cadena del usuario (en este caso, el correo electrónico)
