from django.urls import path
from .views import UserScoreView
app_name='scoring'

urlpatterns = [
    path('user_score/',UserScoreView.as_view(),name='user_score'),
    # path('average_score_update/',AverageScoreUpdateView.as_view(),name='average_score_update'),
]