from rest_framework import serializers
from .models import Panne, Service, Equipement, Utilisateur

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipement
        fields = '__all__'

class PanneSerializer(serializers.ModelSerializer):
    service_nom = serializers.ReadOnlyField(source='service.nom')
    equipement_nom = serializers.ReadOnlyField(source='equipement.nom')

    class Meta:
        model = Panne
        fields = ['id', 'equipement', 'equipement_nom', 'service', 'service_nom', 'description', 'statut', 'cree_le']
