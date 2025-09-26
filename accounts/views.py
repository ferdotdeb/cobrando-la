from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserCreationForm

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # login inmediato tras registro
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})
