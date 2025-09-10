from django.urls import path 
from . import views



urlpatterns = [
    path('', views.index, name = 'index'),
    path('menu/', views.menu, name = 'menu'),
    path('about/', views.about, name = 'about'),
    path('menu-details/<int:pk>/', views.menu_detail, name = 'menu-details'),
    path('blog/', views.blog, name = 'blog'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog-detail'),
    path('contact/', views.contact_us, name = 'contact'),
    path('sign-up/', views.register, name = 'sign-up'),
    
]