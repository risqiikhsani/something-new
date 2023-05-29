
from .models import *
import graphene
from graphene_django import DjangoObjectType

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")

# class IngredientType(DjangoObjectType):
#     class Meta:
#         model = Ingredient
#         fields = ("id", "name", "notes", "category")

class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields = ("id", "user","category","name","detail","price","amount","used_condition","sold","active")

class PhotoType(DjangoObjectType):
    class Meta:
        model = Photo