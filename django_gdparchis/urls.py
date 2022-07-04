from django.urls import path
from gdparchis import views

urlpatterns = [
    path('installation/', views.Installation.as_view()),
    path('game/', views.Game.as_view()),
]
