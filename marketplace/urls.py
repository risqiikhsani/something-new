from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema as schema_without_relay
from .schema_v2 import schema as schema_with_relay

from django.contrib.auth.mixins import LoginRequiredMixin

urlpatterns = [
    # ...
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True,schema=schema_without_relay))),
    path("graphql_relay", csrf_exempt(GraphQLView.as_view(graphiql=True,schema=schema_with_relay))),
]
