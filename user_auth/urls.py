from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts.views import *

urlpatterns = [
    path('register/', views.userRegistration, name='userRegistration'),
    path('login/', views.userLogin, name='userLogin'),
    path('feed/', views.feed, name='feed'),  # <== now we have 'feed' URL
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', views.userLogout, name='logout'),

    path('admin/moderation/', views.adminview, name='adminview'),
    path('admin/block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('admin/unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    # admin urls
    path('admin/posts/<int:post_id>/delete/', views.ad_delete_post, name='ad_delete_post'),

    path('admin/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/block_post/<int:post_id>/', views.block_post, name='block_post'),
    # urls.py
    path('admin/unblock_post/<int:post_id>/', views.unblock_post, name='unblock_post'),

    path('admin/delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('admin/users/<int:user_id>/', views.view_user, name='view_user'),
    path('admin/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post')



]
