from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone', 'display_name')
        labels = {
            'email': 'Email (opcional si proporcionas teléfono)',
            'phone': 'Teléfono (opcional si proporcionas email)',
            'display_name': 'Nombre de usuario/Negocio', # Displayed in the template
        }
        help_texts = {
            'email': 'Proporciona email o teléfono (al menos uno es requerido)',
            'phone': 'Formato: +52XXXXXXXXXX o XXXXXXXXXX',
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")
        
        if not email and not phone:
            raise forms.ValidationError("Debes proporcionar un email o un número de teléfono.")
        
        return cleaned_data

    # Verify that the two password entries match
    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "Raw passwords are not stored, so there is no way to see this user's password, "
        ),
    )

    class Meta:
        model = User
        fields = ('email',
                'phone',
                'password',
                'display_name',
                'public_slug',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                )

    def clean_password(self):
        # Keep the existing hash idk why
        return self.initial["password"]