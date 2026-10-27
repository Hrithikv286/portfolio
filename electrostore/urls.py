"""
ElectroStore URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as error_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('chat/', include('chat.urls')),
]

# Static and media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'electrostore.views.custom_404'
handler500 = 'electrostore.views.custom_500'
