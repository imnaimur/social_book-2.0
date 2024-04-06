from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
# from django.contrib.auth.models import AnonymousUser




# for authenticating email

UserModel = get_user_model()

class AnonymousUser:
    email = None
    is_staff = False
    is_active = False
    is_superuser = False
    # _groups = EmptyManager(Group)
    # _user_permissions = EmptyManager(Permission)

    def __str__(self):
        return self.email

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):

        if email is not None:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        if email is None or password is None:
            return
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        
        else:
            if user.check_password(password):
                return user
        return None
    

