from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from accounts.models import User
from .models import BankDetails

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
    details = BankDetail.objects.filter(owner=request.user).order_by("kind", "-updated_at")
    return render(
        request,
        "bank_details/dashboard.html",
        {"owner": request.user, "details": details},
    )