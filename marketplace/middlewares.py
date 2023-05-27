from django.contrib.auth.models import AnonymousUser
from graphql.execution.middleware import MiddlewareManager

class JWTAuthenticationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        request = info.context

        # Extract JWT token from the request (e.g., from headers or query variables)
        token = extract_token_from_request(request)

        # Authenticate the user based on the token
        user = authenticate_user_from_token(token)

        # Attach the authenticated user to the request
        request.user = user or AnonymousUser()

        # Call the next middleware or resolver
        return next(root, info, **kwargs)

middleware = [
    # ...
    'path.to.JWTAuthenticationMiddleware',
    # ...
]

middleware_manager = MiddlewareManager(*middleware)
