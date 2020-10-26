from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model() 


class Tags(models.Model):
    title = models.CharField(max_length=20)
    color_tags = models.CharField(max_length=20)

    def __str__(self):
        return self.title
 

class Ingredients(models.Model):
    title = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tags, related_name='tags')
    ingredients = models.ManyToManyField(Ingredients, through="Ingredients_recipe")
    cooking_time = models.IntegerField()
    text = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_author')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Ingredients_recipe(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, related_name='ingredient')
    units = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient
