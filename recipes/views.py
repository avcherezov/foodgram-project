from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Tag, Ingredient, Ingredients_recipe, User, Follow, Favorite, ShoppingList
from .forms import RecipeForm
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from .utils import get_ingredients
from django.core.paginator import Paginator


def index(request):
    recipe = Recipe.objects.order_by("-pub_date").all()
    paginator = Paginator(recipe, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for title, units in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                recipe_ingredient = Ingredients_recipe(ingredient=ingredient, units=units, recipe=recipe)
                recipe_ingredient.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, "recipe_new.html", {"form": form})


def profile(request, username):
    recipe = Recipe.objects.filter(author__username=username).order_by("-pub_date").all()
    author = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'recipe': recipe, 'author': author})


def recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})


def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    tag1 = recipe.tag.all()
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
        ingredients = get_ingredients(request)
        if form.is_valid():
            Ingredients_recipe.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for title, units in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                recipe_ingredient = Ingredients_recipe(ingredient=ingredient, units=units, recipe=recipe)
                recipe_ingredient.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipe_edit.html", {"form": form, "tag1": tag1, 'recipe': recipe})


def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('index')


def follow(request):
    recipes_author = Follow.objects.filter(user=request.user)
    return render(request, 'follow.html', {'recipes_author': recipes_author})
 

def favorite(request):
    recipes_favorite = Recipe.objects.filter(favorite_recipe__user__id=request.user.id).all()
    return render(request, 'favorite.html', {'recipes_favorite': recipes_favorite})


def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(request, 'shopping_list.html', {'shopping_list': shopping_list})
