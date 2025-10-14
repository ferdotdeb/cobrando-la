from django.shortcuts import render, redirect

def index(request):
    # Render the home page with user context
    return render(request, 'home/index.html', {
        'user': request.user
    })

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')