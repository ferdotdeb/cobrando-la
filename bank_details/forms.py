from django import forms
from .models import BankDetails

class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ["kind", "value", "bank_name", "alias", "is_public"]
        widgets = {
            "kind": forms.HiddenInput(),
            "value": forms.TextInput(attrs={"placeholder": "Digits only"}),
            "bank_name": forms.TextInput(attrs={"placeholder": "Optional bank name"}),
            "alias": forms.TextInput(attrs={"placeholder": "Optional label"}),
        }

    def save(self, owner, kind, commit=True):
        obj = super().save(commit=False)
        obj.owner = owner
        obj.kind = kind  # Aseguramos que el kind se establezca
        if commit:
            obj.save()  # disparará full_clean() del modelo
        return obj
