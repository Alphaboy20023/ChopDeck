from django.urls import path 
from . import views



urlpatterns = [
    path('', views.index, name = 'index'),
        path('menu/', views.menu, name = 'menu'),
        path('menu-details/<int:pk>/', views.menu_detail, name = 'menu-details'),
        path('about/', views.about, name = 'about'),
        path('blog/', views.blog, name = 'blog'),
        path('blog-detail/<int:pk>/', views.blog_detail, name='blog-detail'),
    path("add-comment/", views.add_comment, name="add-comment"),
    path("cart/", views.cart, name="cart"),
    path("cart/<int:order_id>/", views.cart, name="cart-detail"),
    path("add-to-cart/<int:food_id>/", views.add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<int:food_id>/", views.remove_from_cart, name = "remove-from-cart"),
    path("cart/update/<int:food_id>/", views.update_cart, name="update-cart"),
    path('checkout/', views.checkout, name = 'checkout'),
    path('payment/', views.payment_view, name='payment'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('contact/', views.contact_us, name = 'contact'),
    path('search/', views.search_food, name = 'search'),
    path('sign-up/', views.register, name = 'sign-up'),
    path('login/', views.login, name = 'login'),
    
]

# python manage.py collectstatic
