from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# file_upload
from django import forms


class PostForm(forms.Form):
    image = forms.ImageField(label='イメージ画像', required=False)
