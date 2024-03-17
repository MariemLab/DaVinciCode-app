from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('etudiant', 'Étudiant'),
        ('organisateur', 'Organisateur'),
        ('membre_jury', 'Membre du jury'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='',
        verbose_name='Type d\'utilisateur',
    )

    class Meta:
        permissions = [
            ("can_do_something", "Can do something"),
        ]

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

class Etudiant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    equipe = models.ForeignKey('Equipe', on_delete=models.SET_NULL, null=True)
    niveau_d_etude = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100, choices=(('DSI', 'DSI'), ('CNM', 'CNM'), ('RSS', 'RSS')))
    ROLE_CHOICES = (
        ('membre', 'Membre'),
        ('adjoint', 'Adjoint'),
        ('lead', 'Lead'),
    )
    role_equipe = models.CharField(max_length=20, choices=ROLE_CHOICES, default='membre')

    def __str__(self):
        return self.user.username
    
class Equipe(models.Model):
    id_equipe = models.AutoField(primary_key=True)
    nom_equipe = models.CharField(max_length=100)

class Defi(models.Model):
    id_defi = models.AutoField(primary_key=True)
    titre_defi = models.CharField(max_length=100)
    piece_jointe = models.FileField(upload_to='chemin/vers/dossier', blank=True)
    date_publication = models.DateTimeField(default=datetime.now, blank=True)
    description = models.TextField()
    date_limite = models.DateField()
    STATUT_CHOICES = (
        ('ouvert', 'Ouvert'),
        ('ferme', 'Fermé'),
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ouvert')
    organisateur = models.ForeignKey('Organisateur', on_delete=models.CASCADE)

class Organisateur(models.Model):
    id_organisateur = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='organisateur_user')
    nom_organisateur = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.nom_organisateur
  
class Soumission(models.Model):
    id_soumission = models.AutoField(primary_key=True)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, null=True, blank=True)
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE, null=True, blank=True)
    fichier_soumis = models.FileField(upload_to='submission_files/')
    date_soumission = models.DateTimeField(auto_now_add=True)

class MembreJury(models.Model):
    id_membre_jury = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='jury_user')
    nom_membre = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nom_membre

class Evaluation(models.Model):
    id_evaluation = models.AutoField(primary_key=True)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE)
    membre_jury = models.ForeignKey(MembreJury, on_delete=models.CASCADE, null=True, blank=True, related_name='jury_evaluation')
    note = models.DecimalField(max_digits=5, decimal_places=2)

class GrilleEvaluation(models.Model):
    id_grille = models.AutoField(primary_key=True)
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE, null=True, blank=True, related_name='evaluation_grille')
    critere = models.CharField(max_length=100)
    note_attribuee = models.DecimalField(max_digits=5, decimal_places=2)
    coefficient = models.DecimalField(max_digits=5, decimal_places=2)
