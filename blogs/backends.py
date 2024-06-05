import django.db.models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            # Allow login with either username or email
            user = UserModel.objects.get(Q(username=username) | Q(email=username))
        except UserModel.MultipleObjectsReturned:
            # If multiple users are found, return None to indicate failure
            return None
        except UserModel.DoesNotExist:
            # If no user is found, return None to indicate failure
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None