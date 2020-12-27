from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Tag, Ingredient, Ingredients_recipe, User, Follow, Favorite, ShoppingList
from .forms import RecipeForm
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from .utils import get_ingredients
from django.core.paginator import Paginator
import json
from django.contrib.auth.decorators import login_required


def index(request):
    tags = request.GET.getlist('filters')
    recipe = Recipe.objects.order_by("-pub_date").all()
    if tags:
        recipe = recipe.filter(tag__style__in=tags).distinct().all()
    paginator = Paginator(recipe, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


@login_required
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
    tags = request.GET.getlist('filters')
    recipe = Recipe.objects.filter(author__username=username).order_by("-pub_date").all()
    if tags:
        recipe = recipe.filter(tag__style__in=tags).distinct().all()
        print(recipe)
    author = get_object_or_404(User, username=username)
    paginator = Paginator(recipe, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page, 'author': author})


def recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=username)
    return render(request, 'recipe.html', {'recipe': recipe, 'author': author})


@login_required
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


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('index')


@login_required
def follow(request):
    recipes_author = Follow.objects.filter(user=request.user)
    paginator = Paginator(recipes_author, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page})


@login_required
def follow_add(request):
    author_id = json.loads(request.body)["id"]
    author = get_object_or_404(User, pk=author_id)
    count = Follow.objects.filter(user=request.user).filter(author=author).count()
    if request.user != author:
        if count == 0:
            Follow.objects.create(user=request.user, author=author)
            return JsonResponse({"success": "ok"})


@login_required
def follow_delete(request, author_id):
    user = get_object_or_404(User, username=request.user)
    author = get_object_or_404(User, id=author_id)
    follow = get_object_or_404(Follow, user=user, author=author)
    follow.delete()
    return JsonResponse({"success": True})


@login_required
def favorite(request):
    tags = request.GET.getlist('filters')
    recipes_favorite = Recipe.objects.filter(favorite_recipe__user__id=request.user.id).order_by("-pub_date").all()
    if tags:
        recipes_favorite = recipes_favorite.filter(tag__style__in=tags).distinct().all()
        print(recipe)
    paginator = Paginator(recipes_favorite, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html', {'page': page})


@login_required
def favorite_add(request):
    recipe_id = json.loads(request.body)["id"]
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({"success": True})


@login_required
def favorite_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=request.user.username)
    favorite_recipe = get_object_or_404(Favorite, user=user, recipe=recipe)
    favorite_recipe.delete()
    return JsonResponse({"success": True})


@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(request, 'shopping_list.html', {'shopping_list': shopping_list})


@login_required
def shopping_list_add(request):
    recipe_id = json.loads(request.body)["id"]
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({"success": True})


@login_required
def shopping_list_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=request.user.username)
    shopping_list_recipe = get_object_or_404(ShoppingList, user=user, recipe=recipe)
    shopping_list_recipe.delete()
    return JsonResponse({"success": True})


@login_required
def shopping_list_download(request):
    pass


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500) 
