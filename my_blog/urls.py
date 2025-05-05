from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from user_auth  import  views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_auth.urls')),  # Include user authentication URLs
    path('accounts/', include('accounts.urls')),  # Include accounts URLs
    path('', lambda request: redirect('/auth/login/')),  # ✅ direct to correct full path
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)