from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
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
    email = models.EmailField(unique=True, max_length=25)  
    password = models.CharField(max_length=128)  
    first_name = models.CharField(max_length=30, blank=True)  
    last_name = models.CharField(max_length=30, blank=True)  
    date_joined = models.DateTimeField(default=timezone.now) 
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)  

    # Ejemplo de campo personalizado: foto de perfil
    profile_picture = models.ImageField(
        upload_to='users/images/profile_pictures/',
        default='users/images/profile_pictures/default.png', blank=True
    )
        
    objects = CustomUserManager()  # Instanciamos nuestro administrador personalizado

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = [] 

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email 