from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('index/',views.index,name='index'),
    path('user_register/', views.user_register, name='user_register'),
    path('creer_equipe/', views.creer_equipe, name='creer_equipe'),
    path('soumission/', views.soumission, name='soumission'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('acceuil/',views.acceuil,name='acceuil'),

    path('defis/', views.list_defis, name='list_defis'),
    path('defis/add/', views.add_defi, name='add_defi'),
    path('defis/edit/<int:defi_id>/', views.edit_defi, name='edit_defi'),
    path('defis/delete/<int:defi_id>/', views.delete_defi, name='delete_defi'),

]
