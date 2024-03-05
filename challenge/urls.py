from django.urls import path
from .views import *

app_name = 'challenge'

urlpatterns = [
    path('home/', HomeAPIView.as_view(), name='home'),
    path('challenges/', ChallengesAPIView.as_view(), name='challenges'),
    path('challenges/<id>/', ChallengesDetailAPIView.as_view(), name='challenge_detail'),
    path('challenges/<id>/show/', ChallengesShowAPIView.as_view(), name='challenge_show'),
    path('challenges/<id>/update/', ChallengesUpdateAPIView.as_view(), name='challenge_update'),
]

