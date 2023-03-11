from django.urls import path
from .views import AddToFavoriteView
app_name='favorite'

urlpatterns = [
    path('add_to_favorite/',AddToFavoriteView.as_view(),name='add_to_favorite'),
]