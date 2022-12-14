
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
 path('create/', views.UserCreateView.as_view(), name="create"),
 path('profile/', views.UserProfileView.as_view(), name="profile"),
]
