from django.urls import path
from .views import AddToFavoriteView
app_name='favorite'

urlpatterns = [
    path('',AddToFavoriteView.as_view(),name='favorites'),
]