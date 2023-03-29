from django.urls import path
from .views import status_shop_card,ShopCardView,show_shop_card,add_to_shop_card,delete_from_shop_card,add_more_product
app_name='orders'

urlpatterns = [
    path('status_shop_card/',status_shop_card,name='status_shop_card'),
    path('shop_cards/',ShopCardView.as_view(),name='shop_cards'),
    path('show_shop_cards/',show_shop_card,name='show_shop_cards'),
    path('add_to_shop_card/',add_to_shop_card,name='add_to_shop_card'),
    path('delete_form_shop_card/',delete_from_shop_card,name='delete_form_shop_card'),
    path('add_more_product/',add_more_product,name='add_more_product'),



]