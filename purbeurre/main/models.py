from django.db import models
from django.contrib.auth.models import User


class Aliment(models.Model):
    """
    This class represents all the informations
    fetched from the REST API of the
    OpenFoodFact project
    """

    name = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200)
    date = models.TextField(max_length=100)
    brands = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=100)
    ingredients = models.TextField()
    image = models.URLField(max_length=255)
    url = models.URLField(max_length=255)
    stores = models.CharField(max_length=300)
    quantity = models.CharField(max_length=300)
    packaging = models.CharField(max_length=600)
    ingredients_fr = models.TextField()
    manufactured_places = models.CharField(max_length=1000)
    purchase_places = models.CharField(max_length=500)
    categories = models.TextField()
    code = models.CharField(max_length=200)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """
    This class is used to associate the aliments saved
    by a specific User
    """

    saved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.saved_by} -- {self.saved_aliment}"
