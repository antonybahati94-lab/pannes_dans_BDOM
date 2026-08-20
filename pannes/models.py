from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Modèle pour le Site / Service (ex: Kadutu, Ibanda, BDOM Central)
class Service(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# 2. Modèle Utilisateur personnalisé avec rôle et service rattaché
class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('agent', 'Agent de Service'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

# 3. Modèle Équipement
class Equipement(models.Model):
    nom = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.service.nom}"

# 4. Modèle Panne
class Panne(models.Model):
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    statut = models.CharField(max_length=50, default='En attente')
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panne #{self.id} - {self.description[:20]}"