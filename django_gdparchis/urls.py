from django.urls import path, include
from gdparchis import views
from gdparchis import views as gdparchis_views
from rest_framework import routers

router = routers.DefaultRouter()
routers.DefaultRouter
router.register(r'game', gdparchis_views.GameViewSet)
router.register(r'state', gdparchis_views.StateViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('installations/', views.InstallationAPIView.as_view()),
    path('games/', views.GameAPIView.as_view()),
    path('statistics/globals/', views.StatisticsGlobal),
    path('statistics/user/', views.StatisticsUser),
]
