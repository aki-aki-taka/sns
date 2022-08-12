from django.urls import path
from .views import Home, MyPost, DetailPost, CreatePost, UpdatePost, DeletePost, FollowHome, FollowDetail, FollowList
from . import views

app_name = 'base'

urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('', views.TopView.as_view(), name='top'),
    path('mypost/', MyPost.as_view(), name='mypost'),
    path('home/category/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('detail/<int:pk>/', DetailPost.as_view(), name='detail'),
    path('detail/<int:pk>/update/', UpdatePost.as_view(), name='update'),
    path('detail/<int:pk>/delete/', DeletePost.as_view(), name='delete'),
    path('create/', CreatePost.as_view(), name='create'),
    path('follow-home/<int:pk>', FollowHome.as_view(), name='follow-home'),
    path('follow-detail/<int:pk>', FollowDetail.as_view(), name='follow-detail'),
    path('follow-list/', FollowList.as_view(), name='follow-list'),
]
