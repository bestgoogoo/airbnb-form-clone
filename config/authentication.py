from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class TestAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(request.headers)
        username = request.headers.get("Username")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"Doesn`t exist {username}")
