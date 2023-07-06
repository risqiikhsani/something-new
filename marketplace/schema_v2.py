# cookbook/ingredients/schema.py
from graphene import relay
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .types_v2 import *


class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    # ingredient = relay.Node.Field(IngredientNode)
    # all_ingredients = DjangoFilterConnectionField(IngredientNode)

class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,mutation=Mutation)
