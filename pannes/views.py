from rest_framework import viewsets, permissions
from .models import Service, Equipement, Panne
from .serializers import ServiceSerializer, EquipementSerializer, PanneSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Si c'est l'administrateur / superutilisateur
        if user.is_staff or getattr(user, 'role', '') == 'ADMIN':
            return Equipement.objects.all()
        # Si l'utilisateur appartient à un service/site
        if hasattr(user, 'service') and user.service:
            return Equipement.objects.filter(service=user.service)
        return Equipement.objects.none()


class PanneViewSet(viewsets.ModelViewSet):
    serializer_class = PanneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # 1. Administrateur : Accès à toutes les pannes
        if user.is_staff or getattr(user, 'role', '') == 'ADMIN':
            return Panne.objects.all().order_by('-id')
        
        # 2. Agent de site : Accès uniquement aux pannes de son propre service/site
        if hasattr(user, 'service') and user.service:
            return Panne.objects.filter(equipement__service=user.service).order_by('-id')
            
        # Par défaut : Aucun résultat si aucun service n'est associé
        return Panne.objects.none()

    def perform_create(self, serializer):
        # Associe automatiquement l'utilisateur connecté lors de la déclaration d'une panne
        serializer.save(déclaré_par=self.request.user)