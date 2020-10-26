from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Tags, Ingredients, Ingredients_recipe
from .forms import RecipeForm
from django.views.generic import View
from django.http import JsonResponse, HttpResponse


def index(request):
    recipe = Recipe.objects.order_by("-pub_date").all()
    return render(request, 'index.html', {'recipe': recipe})

def new_recipe(request):
    tag = Tags.objects.order_by("id").all()
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('index')
    else:
        form = RecipeForm(request.POST or None, files=request.FILES or None)
    return render(request, "recipe_new.html", {"form": form, "tag": tag})
