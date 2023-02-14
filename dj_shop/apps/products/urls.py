from django.urls import path
from .views import cheapest_product,newest_product,favorite_product,related_product,ProductGroupView
app_name='products'

urlpatterns = [
    path('cheapest_product/',cheapest_product,name='cheapest_product'),
    path('newest_product/',newest_product,name='newest_product'),
    path('favorite_product/',favorite_product,name='favorite_Product'),
    path('related_product/<slug:slug>/',related_product,name='related_product'),
    path('product_group/',ProductGroupView.as_view(),name='product_group'),

]