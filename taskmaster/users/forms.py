from django import forms

from .models import CustomUser


class UserForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "custom-input",
                "placeholder": "Ingresa tu correo electrónico",
                "autocomplete": "email",
            }
        ),
        # Habilitar el autocompletado para el campo de correo electrónico
        required=True,
        label="Correo electrónico",
        max_length=254,
        help_text="Requerido. 254 caracteres o menos. Debe ser una dirección de correo electrónico válida.",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "custom-input",
                "placeholder": "Ingresa tu contraseña",
                "autocomplete": "current-password",
            }
        ),
        # Habilitar el autocompletado para el campo de contraseña
        required=True,
        label="Contraseña",
        max_length=128,
        help_text="Requerido. 128 caracteres o menos. Debe ser seguro.",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "custom-input",
                "placeholder": "Ingresa de nuevo la misma contraseña",
                "autocomplete": "current-password",
            }
        ),
        # Habilitar el autocompletado para el campo de contraseña
        required=True,
        label="Contraseña 2",
        max_length=128,
        help_text="Requerido. 128 caracteres o menos. Debe ser seguro.",
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "custom-input", "placeholder": "Ingresa tu nombre"}
        ),
        # Habilitar el autocompletado para el campo de nombre
        label="Nombre",
        max_length=30,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "custom-input", "placeholder": "Ingresa tu apellido"}
        ),
        # Habilitar el autocompletado para el campo de apellido
        label="Apellido",
        max_length=30,
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        existing_user = (
            CustomUser.objects.filter(email=email)
            .exclude(pk=self.instance.pk if self.instance else None)
            .first()
        )

        if existing_user:
            raise forms.ValidationError(
                "Este correo electrónico ya está en uso. Por favor, elige otro."
            )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Las contraseñas no coinciden. Por favor, inténtalo de nuevo."
            )

        return password2

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "profile_picture",
        )

        labels = {
            "email": "Correo Electrónico",
            "password1": "Contraseña",
            "password2": "Repetir Contraseña",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "profile_picture": "Foto de Perfil",
        }


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "custom-input",
                "placeholder": "Ingresa tu correo electrónico",
                "autocomplete": "email",
            }
        ),
        # Habilitar el autocompletado para el campo de correo electrónico
        required=True,
        label="Correo electrónico",
        max_length=254,
        help_text="Requerido. 254 caracteres o menos. Debe ser una dirección de correo electrónico válida.",
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "custom-input", "placeholder": "Ingresa tu nombre"}
        ),
        # Habilitar el autocompletado para el campo de nombre
        required=True,
        label="Nombre",
        max_length=30,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "custom-input", "placeholder": "Ingresa tu apellido"}
        ),
        # Habilitar el autocompletado para el campo de apellido
        required=True,
        label="Apellido",
        max_length=30,
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "profile_picture")

        labels = {
            "email": "Correo Electrónico",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "profile_picture": "Foto de Perfil",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        existing_user = (
            CustomUser.objects.filter(email=email)
            .exclude(pk=self.instance.pk if self.instance else None)
            .first()
        )

        if existing_user:
            raise forms.ValidationError(
                "Este correo electrónico ya está en uso. Por favor, elige otro."
            )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Las contraseñas no coinciden. Por favor, inténtalo de nuevo."
            )

        return password2

