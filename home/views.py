from django.shortcuts import render, redirect

def index(request):
    # If the user is authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')  # The dashboard is the main view after login
    
    return render(request, 'home/index.html')