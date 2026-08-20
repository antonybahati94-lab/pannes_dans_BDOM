from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ServiceViewSet, EquipementViewSet, PanneViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'equipements', EquipementViewSet, basename='equipement')
router.register(r'pannes', PanneViewSet, basename='panne')

urlpatterns = [
    # Route de connexion pour votre login.html
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Routes du routeur pour l'API
    path('', include(router.urls)),
]