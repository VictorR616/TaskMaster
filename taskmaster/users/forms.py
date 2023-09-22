from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Ingresa tu correo electrónico', 'autocomplete': 'email'}),
        # Habilitar el autocompletado para el campo de correo electrónico
        required=True,
        label='Correo electrónico',
        max_length=254,
        help_text='Requerido. 254 caracteres o menos. Debe ser una dirección de correo electrónico válida.',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'custom-input', 'placeholder': 'Ingresa tu contraseña', 'autocomplete': 'current-password'}),
        # Habilitar el autocompletado para el campo de contraseña
        required=True,
        label='Contraseña',
        max_length=128,
        help_text='Requerido. 128 caracteres o menos. Debe ser seguro.',
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Ingresa tu nombre'}),
        # Habilitar el autocompletado para el campo de nombre
        required=True,
        label='Nombre',
        max_length=30,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Ingresa tu apellido'}),
        # Habilitar el autocompletado para el campo de apellido
        required=True,
        label='Apellido',
        max_length=30,
    )
    profile_picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'custom-input'}),
        # Habilitar el autocompletado para el campo de imagen de perfil
        label='Imagen de perfil',
    )

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

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Ingresa tu correo electrónico', 'autocomplete': 'email'}),
        # Habilitar el autocompletado para el campo de correo electrónico
        required=True,
        label='Correo electrónico',
        max_length=254,
        help_text='Requerido. 254 caracteres o menos. Debe ser una dirección de correo electrónico válida.',
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Ingresa tu nombre'}),
        # Habilitar el autocompletado para el campo de nombre
        required=True,
        label='Nombre',
        max_length=30,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Ingresa tu apellido'}),
        # Habilitar el autocompletado para el campo de apellido
        required=True,
        label='Apellido',
        max_length=30,
    )
    profile_picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'custom-input'}),
        # Habilitar el autocompletado para el campo de imagen de perfil
        label='Imagen de perfil',
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'profile_picture')
        
        labels = {
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'profile_picture': 'Foto de Perfil',
        }

