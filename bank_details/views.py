from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from .models import BankDetails
from .forms import BankDetailsForm

def public_profile(request, public_slug: str):
    user = get_object_or_404(User, public_slug=public_slug, is_active=True)
    details = (
        BankDetails.objects.filter(owner=user, is_public=True)
        .order_by("kind", "-updated_at")
    )
    return render(
        request,
        "bank_details/public_profile.html",
        {"owner": user, "details": details},
    )

@login_required
def dashboard(request):
    Kind = BankDetails.Kind

    kind_labels = {
        Kind.CLABE: "CLABE interbancaria",
        Kind.CARD: "Tarjeta de débito",
        Kind.ACCOUNT: "Cuenta bancaria",
    }

    def _get_instance(k):
        return BankDetails.objects.filter(owner=request.user, kind=k).first()

    clabe_inst = _get_instance(Kind.CLABE)
    card_inst = _get_instance(Kind.CARD)
    acct_inst = _get_instance(Kind.ACCOUNT)

    if request.method == "POST":
        form_kind = request.POST.get("form_kind")
        if form_kind not in {Kind.CLABE, Kind.CARD, Kind.ACCOUNT}:
            messages.error(request, "Tipo de formulario inválido.")
            return redirect("dashboard")

        # Escoge la instancia según el kind:
        inst_map = {
            Kind.CLABE: clabe_inst,
            Kind.CARD: card_inst,
            Kind.ACCOUNT: acct_inst,
        }
        instance = inst_map[form_kind]

        # Crear una copia mutable del POST data y agregar el kind
        post_data = request.POST.copy()
        post_data['kind'] = form_kind
        
        form = BankDetailsForm(post_data, instance=instance)
        if form.is_valid():
            try:
                form.save(owner=request.user, kind=form_kind)
                messages.success(request, f"{kind_labels[form_kind]} guardada correctamente.")
                return redirect("dashboard")  # PRG: evita re-envíos
            except Exception as e:
                messages.error(request, f"Error al guardar: {e}")
        else:
            messages.error(request, "Por favor, corrija los errores a continuación.")
        # Si hay errores, volvemos a construir los otros forms "en limpio"
        other_forms = {
            Kind.CLABE: BankDetailsForm(instance=clabe_inst, initial={'kind': Kind.CLABE}),
            Kind.CARD: BankDetailsForm(instance=card_inst, initial={'kind': Kind.CARD}),
            Kind.ACCOUNT: BankDetailsForm(instance=acct_inst, initial={'kind': Kind.ACCOUNT}),
        }
        other_forms[form_kind] = form  # conserva el que tiene errores
        return render(
            request,
            "bank_details/dashboard.html",
            {
                "owner": request.user,
                "forms": other_forms,
                "instances": {"clabe": clabe_inst, "card": card_inst, "account": acct_inst},
            },
        )

    # GET
    forms = {
        Kind.CLABE: BankDetailsForm(instance=clabe_inst, initial={'kind': Kind.CLABE}),
        Kind.CARD: BankDetailsForm(instance=card_inst, initial={'kind': Kind.CARD}),
        Kind.ACCOUNT: BankDetailsForm(instance=acct_inst, initial={'kind': Kind.ACCOUNT}),
    }
    return render(
        request,
        "bank_details/dashboard.html",
        {
            "owner": request.user,
            "forms": forms,
            "instances": {"clabe": clabe_inst, "card": card_inst, "account": acct_inst},
        },
    )