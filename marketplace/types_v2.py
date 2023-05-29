# cookbook/ingredients/schema.py
from graphene import relay
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import *


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name']
        interfaces = (relay.Node, )


# class IngredientNode(DjangoObjectType):
#     class Meta:
#         model = Ingredient
#         # Allow for some more advanced filtering here
#         filter_fields = {
#             'name': ['exact', 'icontains', 'istartswith'],
#             'notes': ['exact', 'icontains'],
#             'category': ['exact'],
#             'category__name': ['exact'],
#         }
#         interfaces = (relay.Node, )