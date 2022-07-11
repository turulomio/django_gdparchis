from django.urls import path
from gdparchis import views

urlpatterns = [
    path('installations/', views.InstallationAPIView.as_view()),
    path('games/', views.GameAPIView.as_view()),
    path('statistics/globals/', views.StatisticsGlobal),
    path('statistics/user/', views.StatisticsUser),
]
