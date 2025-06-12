from django.contrib.auth import get_user_model
from django.contrib.auth.backends import  BaseBackend


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        model = get_user_model()
        try:
            user = model.objects.get(email=username)
        except (model.DoesNotExist, model.MultipleObjectsReturned):
            return None
        if user.check_password(password):
            return user


    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except:
            return None