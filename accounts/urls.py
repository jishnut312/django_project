from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
  
    path('post/create/', views.post_create, name='post_create'),
    # other URLs...
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_pk>/comment/edit/<int:comment_pk>/',views.edit_comment, name='edit_comment'),    
    path('comment/delete/<int:post_pk>/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
    path('profile/', views.profile, name='profile'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)