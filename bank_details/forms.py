from django import forms
from .models import BankDetails

class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ["kind", "value", "bank_name", "alias", "phone", "is_public"]
        widgets = {
            "kind": forms.HiddenInput(),
            "value": forms.TextInput(attrs={"placeholder": "Escribe numeros unicamente"}),
            "bank_name": forms.TextInput(attrs={"placeholder": "Nombre del banco (opcional)"}),
            "alias": forms.TextInput(attrs={"placeholder": "Alias (opcional)"}),
            "phone": forms.TextInput(attrs={"placeholder": "Ej: 9981234567 o +529981234567"}),
        }

    def save(self, owner, kind, commit=True):
        obj = super().save(commit=False)
        obj.owner = owner
        obj.kind = kind  # Aseguramos que el kind se establezca
        if commit:
            obj.save()  # disparará full_clean() del modelo
        return obj
