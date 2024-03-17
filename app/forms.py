from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.decorators import login_required

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=255, label="Nom d'utilisateur")
    email = forms.EmailField(label="Adresse email")
    password1 = forms.CharField(max_length=255, label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=255, label="Confirmez le mot de passe", widget=forms.PasswordInput)
    niveau_d_etude = forms.CharField(max_length=100, label="Niveau d'étude", required=False)
    specialite = forms.CharField(max_length=100, label="Spécialité", required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'niveau_d_etude', 'specialite']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmez le mot de passe"

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'etudiant'  # Attribuer le rôle "étudiant" par défaut
        if commit:
            user.save()
        return user

class EquipeCreationForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['nom_equipe']

    leader = forms.ModelChoiceField(queryset=Etudiant.objects.filter(role_equipe='lead'), label="Leader")
    adjoint = forms.ModelChoiceField(queryset=Etudiant.objects.filter(role_equipe='adjoint'), label="Adjoint")
    membres = forms.ModelMultipleChoiceField(queryset=Etudiant.objects.all(), label="Membres de l'équipe", required=False)

    def clean_membres(self):
        membres = self.cleaned_data['membres']
        leader = self.cleaned_data.get('leader')
        adjoint = self.cleaned_data.get('adjoint')
        
        # Ajout du leader et de l'adjoint à la liste des membres
        membres = list(membres) + [leader, adjoint]

        if len(membres) < 6 or len(membres) > 8:
            raise forms.ValidationError("Le nombre total de membres d'une équipe, y compris le leader et l'adjoint, doit être entre 6 et 8.")
        
        return membres
      
from django import forms
from .models import Soumission

class SoumissionForm(forms.ModelForm):
    def __init__(self, *args, defi_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if defi_choices:
            self.fields['defi'] = forms.ChoiceField(choices=defi_choices, label='Choisissez un défi')

    class Meta:
        model = Soumission
        fields = ['defi', 'fichier_soumis']

class DefiForm(forms.ModelForm):
        class Meta:
            model = Defi
            fields = ['titre_defi', 'piece_jointe','description', 'date_limite', 'organisateur']
            widgets = {
            'date_limite': forms.DateInput(attrs={'type': 'date'})
        }