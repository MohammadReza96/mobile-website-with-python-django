from django.urls import path
from .views import AddToFavoriteView,FavoriteProductView
app_name='favorite'

urlpatterns = [
    path('add_to_favorite/',AddToFavoriteView.as_view(),name='add_to_favorite'),
    path('favorite_product_list/',FavoriteProductView.as_view(),name='favorite_product_list'),
]