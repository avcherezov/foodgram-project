from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Tags, Ingredients, Ingredients_recipe, User
from .forms import RecipeForm
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from .utils import get_ingredients


def index(request):
    recipe = Recipe.objects.order_by("-pub_date").all()
    return render(request, 'index.html', {'recipe': recipe})


def new_recipe(request):
    tag = Tags.objects.order_by("id").all()
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'ингредиенты не найдены')
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for title, units in ingredients.items():
                ingredient = get_object_or_404(Ingredients, title=title)
                recipe_ingredient = Ingredients_recipe(ingredient=ingredient, units=units, recipe=recipe)
                recipe_ingredient.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm(request.POST or None, files=request.FILES or None)
    return render(request, "recipe_new.html", {"form": form, "tag": tag})


def profile(request, username):
    recipe = Recipe.objects.filter(author__username=username).order_by("-pub_date").all()
    author = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'recipe': recipe, 'author': author})


def recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})

