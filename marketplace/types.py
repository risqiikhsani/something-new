
from .models import Category, Ingredient, Item, Photo
import graphene
from graphene_django import DjangoObjectType

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")

class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields = ("id", "user","category","name","detail","price","amount","used_condition","sold","active")

class PhotoType(DjangoObjectType):
    class Meta:
        model = Photo