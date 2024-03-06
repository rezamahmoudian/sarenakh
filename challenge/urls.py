from django.urls import path
from .views import *

app_name = 'challenge'

urlpatterns = [
    path('home', HomeAPIView.as_view(), name='home'),
    path('profile/<user_id>', ProfileAPIView.as_view(), name='home'),
    path('challenges', ChallengesAPIView.as_view(), name='challenges'),
    # path('challenge/<id>/', ChallengesDetailAPIView.as_view(), name='challenge_detail'),
    path('challenge/<id>/user/<user_id>', ChallengesDetailUserAPIView.as_view(), name='challenge_detail'),
    path('challenge/<id>/user/<user_id>/show', ChallengesShowAPIView.as_view(), name='challenge_show'),
    path('challenge/<id>/user/<user_id>/update', ChallengesUpdateAPIView.as_view(), name='challenge_update'),
]

