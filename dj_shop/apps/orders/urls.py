from django.urls import path
from .views import status_shop_card
app_name='orders'

urlpatterns = [
    path('status_shop_card/',status_shop_card,name='status_shop_card'),
]