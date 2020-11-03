from django.contrib import admin
from .models import Recipe, Tags, Ingredients, Ingredients_recipe


class Ingredients_recipeInline(admin.TabularInline):
    model = Ingredients_recipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", 'title', 'cooking_time', 'text', 'author', 'pub_date') 
    empty_value_display = '-пусто-'
    inlines = (Ingredients_recipeInline,)


class TagsAdmin(admin.ModelAdmin):
    list_display = ("pk", 'title', 'color_tags') 
    empty_value_display = '-пусто-'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ("pk", 'title', 'dimension') 
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
