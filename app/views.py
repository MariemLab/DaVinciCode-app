
# Create your views here.
from django.db import transaction
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm,EquipeCreationForm,DefiForm
from .models import CustomUser, Etudiant, Organisateur, MembreJury,Defi
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login,logout
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm,SoumissionForm
from .models import CustomUser, Etudiant, Organisateur, MembreJury,Defi
from django.contrib.auth.decorators import login_required

def index(request):
    etudiants = Etudiant.objects.all()

    # Passer les étudiants au template dans le contexte de rendu
    return render(request, 'index.html', {'etudiants': etudiants})

def acceuil(request):
    return render(request, 'acceuil.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # Correction ici
            if user is not None:
                auth_login(request, user)
                return redirect('acceuil')
            else:
                # Gérer le cas où l'authentification échoue
                return render(request, 'login.html', {'form': form, 'error_message': 'Identifiants invalides.'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@transaction.atomic
def user_register(request):
    errors = []
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            if CustomUser.objects.filter(username=username).exists():
                errors.append("Le nom d'utilisateur est déjà utilisé.")
            else:
                user = form.save(commit=False)
                role = form.cleaned_data.get('role')
                user.save()
                # Sauvegarde du rôle dans le modèle approprié
                
                etudiant_data = {
                        'user': user,
                        'niveau_d_etude': form.cleaned_data.get('niveau_d_etude'),
                        'specialite': form.cleaned_data.get('specialite'),
                }
                etudiant = Etudiant.objects.create(**etudiant_data)
                etudiant.save()
                

                messages.success(request, 'Inscription réussie. Bienvenue!')
                return redirect('user_login')
        else:
            # Gérer les erreurs du formulaire
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form, 'errors': errors})


def creer_equipe(request):
    if request.method == 'POST':
        nom_equipe = request.POST.get('nom_equipe')
        
        leader_id_str = request.POST.get('leader')
        if leader_id_str:
            leader_id = int(leader_id_str)
        else:
            leader_id = None  # Définir leader_id comme None si l'ID du leader est vide
        
        adjoint_id_str = request.POST.get('adjoint')
        if adjoint_id_str:
            adjoint_id = int(adjoint_id_str)
        else:
            adjoint_id = None  # Définir adjoint_id comme None si l'ID de l'adjoint est vide
        
        # Récupération des instances d'étudiants pour le leader et l'adjoint
        leader = Etudiant.objects.get(user_id=leader_id) if leader_id else None
        adjoint = Etudiant.objects.get(user_id=adjoint_id) if adjoint_id else None
        
        # Récupération des IDs des membres de l'équipe
        membres_ids = [request.POST.get(f'membre_{i}') for i in range(1, 5)]
        membres_ids = [int(id) for id in membres_ids if id]  # Convertir les IDs non vides en entiers
        
        membres = []
        for membre_id in membres_ids:
            try:
                membre = Etudiant.objects.get(user_id=membre_id)
                membres.append(membre)
            except Etudiant.DoesNotExist:
                messages.error(request, f"L'étudiant avec l'ID {membre_id} n'existe pas.")
                return redirect('creer_equipe')

        # Vérification des niveaux d'études du leader et de l'adjoint
        if leader.niveau_d_etude == adjoint.niveau_d_etude:
            messages.error(request, "Le leader et l'adjoint doivent avoir des niveaux d'études différents.")
            return redirect('creer_equipe')
        
        # Vérification du nombre total de membres, y compris le leader et l'adjoint
        total_membres = len(membres) + 2
        if total_membres < 6 or total_membres > 8:
            messages.error(request, "Le nombre total de membres, y compris le leader et l'adjoint, doit être entre 6 et 8.")
            return redirect('creer_equipe')

        # Vérification des spécialités
        specialites = set([membre.specialite for membre in membres])
        if len(specialites) < 3:
            messages.error(request, "Il doit y avoir au moins un étudiant de chaque spécialité (DSI, CNM, RSS).")
            return redirect('creer_equipe')

        # Vérification des étudiants de niveau L2
        etudiants_L2 = [membre for membre in membres if membre.niveau_d_etude == 'L2']
        if len(etudiants_L2) < 4:
            messages.error(request, "Il doit y avoir au moins quatre étudiants de L2 dans l'équipe.")
            return redirect('creer_equipe')

        # Vérification qu'un étudiant ne soit pas dans deux équipes différentes
        for membre in membres:
            if membre.equipe is not None:
                messages.error(request, "Un étudiant ne peut être dans deux équipes différentes.")
                return redirect('creer_equipe')

        # Création de l'équipe
        equipe = Equipe.objects.create(nom_equipe=nom_equipe)

        # Attribution du leader et de l'adjoint à l'équipe
        leader.role_equipe = 'lead'
        leader.equipe = equipe
        leader.save()

        adjoint.role_equipe = 'adjoint'
        adjoint.equipe = equipe
        adjoint.save()

        # Attribution des membres à l'équipe
        for membre in membres:
            membre.role_equipe = 'membre'
            membre.equipe = equipe
            membre.save()

        messages.success(request, "L'équipe a été créée avec succès.")
        return redirect('page_suivante')  # Rediriger vers la page suivante après la création de l'équipe

    else:
        # Gérer le cas où la méthode HTTP n'est pas POST
        return redirect(creer_equipe)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Vous êtes déconnecté avec succès.')
    else:
        # Si l'utilisateur n'est pas authentifié, vous pouvez afficher un message d'erreur ou effectuer d'autres actions.
        messages.error(request, 'Vous n\'êtes pas connecté.')
    return redirect('user_login')

from django.http import JsonResponse

@login_required(login_url='user_login') 
def soumission(request):
    if request.method == 'POST':
        form = SoumissionForm(request.POST, request.FILES)
        if form.is_valid():
            etudiant = request.user.etudiant  # Récupérer l'étudiant connecté
            equipe_id = etudiant.equipe_id  # Récupérer l'ID de l'équipe de l'étudiant
            soumission = form.save(commit=False)
            soumission.equipe_id = equipe_id  # Enregistrer l'ID de l'équipe avec la soumission
            soumission.save()
            return JsonResponse({'success': True})
    else:
        defi_choices = Defi.objects.values_list('id_defi', 'titre_defi')
        form = SoumissionForm(defi_choices=defi_choices)
    return render(request, 'soumission.html', {'form': form})

def list_defis(request):
    defis = Defi.objects.all()
    return render(request, 'list_defis.html', {'defis': defis})

def add_defi(request):
    if request.method == 'POST':
        form = DefiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('acceuil')
    else:
        form = DefiForm()
    return render(request, 'add_defi.html', {'form': form})

def edit_defi(request, defi_id):
    defi = get_object_or_404(Defi, pk=defi_id)
    if request.method == 'POST':
        form = DefiForm(request.POST, instance=defi)
        if form.is_valid():
            form.save()
            return redirect('list_defis')
    else:
        form = DefiForm(instance=defi)
    return render(request, 'edit_defi.html', {'form': form, 'defi': defi})

def delete_defi(request, defi_id):
    defi = get_object_or_404(Defi, pk=defi_id)
    defi.delete()
    return redirect('list_defis')