from django.urls import path 
from . import views



urlpatterns = [
    path('chopdeck/', views.index, name = 'index'),
    path('chopdeck/menu/', views.menu, name = 'menu'),
    path('chopdeck/about/', views.about, name = 'about'),
    path('chopdeck/menu-details/<int:pk>/', views.menu_detail, name = 'menu-details'),
    path('chopdeck/blog/', views.blog, name = 'blog'),
    path('chopdeck/blogs/<int:pk>/', views.blog_detail, name='blog-detail'),
    path('chopdeck/contact/', views.contact_us, name = 'contact'),
    path('chopdeck/sign-up/', views.register, name = 'sign-up'),
    path('chopdeck/login/', views.login, name = 'login'),
    
]

# python manage.py collectstatic
