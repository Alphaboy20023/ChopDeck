from django.urls import path 
from . import views

from ChopDeck import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('menu/', views.menu, name = 'menu'),
    path('about/', views.about, name = 'about'),
    path('blog/', views.blog, name = 'blog'),
    path('contact/', views.contact_us, name = 'contact'),
    path('sign-up/', views.register, name = 'sign-up'),
    
] + static(settings.MEDIA_URL,
           document_root = settings.MEDIA_ROOT)