from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Service, Utilisateur, Equipement, Panne

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations BDOM', {'fields': ('role', 'service')}),
    )
    list_display = ('username', 'email', 'role', 'service', 'is_staff')

@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'service')

@admin.register(Panne)
class PanneAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipement', 'service', 'statut', 'cree_le')
    list_filter = ('service', 'statut')