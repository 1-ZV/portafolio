from django.shortcuts import render
from .models import Project

def index(request):
    projects = Project.objects.all()
    return render(request, "app_portafolio/index.html", {'projects':projects})
