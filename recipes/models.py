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
    tags = models.ManyToManyField(Tags)
    ingredients = models.ManyToManyField(Ingredients)
    cooking_time = models.IntegerField()
    text = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_author')
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title
