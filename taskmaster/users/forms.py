from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Configura el campo de contraseña como campo de contraseña

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'profile_picture')
        
        labels = {
            'email': 'Correo Electrónico',
            'password':  'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'profile_picture': 'Foto de Perfil',
        }

