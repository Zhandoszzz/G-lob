from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_post/', add_post, name='add_post'),
    path('search/', search, name='search'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('category/<name>', category, name='category'),
    path('post/delete/<id>', delete_post, name='delete_post'),
    path('post/edit/<id>', edit_post, name='edit_post'),
    path('post/<id>', get_post, name='post'),
    path('post/<id>/comment', comment, name='comment'),
    path('add/category', add_category, name='add_category')
]