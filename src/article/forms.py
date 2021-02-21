from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCreationFormInModel(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")


class UserChangeFormInModel(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "username")
