from django.shortcuts import render
from .models import Recipe


def index(request):
    recipe = Recipe.objects.order_by("-pub_date").all()
    return render(request, 'index.html', {'recipe': recipe})
