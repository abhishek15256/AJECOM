from django.urls import path

from .views import checkoutpage, ProductView, HomeView, add_to_cart, remove_from_cart, login_view, CartView

app_name = 'core'

urlpatterns = [
    path('home/', HomeView.as_view(), name= "homepage"),
    path('', HomeView.as_view(),name="homepage"),
    path('checkout/', checkoutpage),
    path('login/', login_view, name='login'),
    path('cart/', CartView.as_view(), name='cart'),
    path('product/<slug>/', ProductView.as_view(), name="product"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
]
