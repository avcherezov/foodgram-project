from django.forms import ModelForm
from .models import Recipe
from django.forms import CheckboxSelectMultiple


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'cooking_time', 'text', 'image']
        widgets = {'tag': CheckboxSelectMultiple()}
