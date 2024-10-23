from django.urls import path
from .views import *

urlpatterns = [
    path('postes/', PosteAttacheListView.as_view(), name='postes_list'),
    path('postes/<int:pk>/', PosteAttacheDetailView.as_view(), name='poste_detail'),
    path('perceptors/', PerceptorListView.as_view(), name='perceptors_list'),
    path('perceptors/<int:pk>/', PerceptorDetailView.as_view(), name='perceptor_detail'),

    # Utilisateur URLs
    path('utilisateur/', UtilisateurListView.as_view(), name='utilisateur-list'),
    path('utilisateur/<int:pk>/', UtilisateurDetailView.as_view(), name='utilisateur-detail'),

    # Role URLs
    path('role/', RoleListView.as_view(), name='role-list'),
    path('role/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),

    # UserRole URLs
    path('user-role/', UserRoleListView.as_view(), name='user-role-list'),
    path('user-role/<int:pk>/', UserRoleDetailView.as_view(), name='user-role-detail'),
]
