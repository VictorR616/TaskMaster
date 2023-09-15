from django import forms
from users.models import CustomUser  # Asegúrate de importar el modelo de usuario personalizado

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'profile_picture', 'is_active', 'is_staff')
