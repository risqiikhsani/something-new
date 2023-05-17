

from .models import Category, Ingredient
import graphene
from graphene_django import DjangoObjectType
from .types import *
from .models import *

class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None
        
# class QuestionType(DjangoObjectType):
#     class Meta:
#         model = Question
        
# class QuestionMutation(graphene.Mutation):
#     class Arguments:
#         # The input arguments for this mutation
#         text = graphene.String(required=True)
#         id = graphene.ID()

#     # The class attributes define the response of the mutation
#     question = graphene.Field(QuestionType)

#     @classmethod
#     def mutate(cls, root, info, text, id):
#         question = Question.objects.get(pk=id)
#         question.text = text
#         question.save()
#         # Notice we return an instance of this mutation
#         return QuestionMutation(question=question)


# class Mutation(graphene.ObjectType):
#     update_question = QuestionMutation.Field()

class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,mutation=Mutation)

# class Query(graphene.ObjectType):
#     hello = graphene.String(default_value="Hi!")

# schema = graphene.Schema(query=Query)