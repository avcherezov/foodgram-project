from django.forms import ModelForm
from .models import Recipe
from django.forms import CheckboxSelectMultiple


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'cooking_time', 'text', 'image']
        widgets = {'tags': CheckboxSelectMultiple()}
