from django.urls import path
from . import views

urlpatterns = [    
    path('', views.registration, name="registration"),
    path('delegate/<int:delegate_id>/', views.displayDelegate, name="displayDelegate"),
    path('registration_ind/', views.registrationInd, name="registrationInd"),
    path('delegation/<int:delegation_id>/', views.displayDelegation, name="displayDelegation"),
    path('registration_team/', views.registrationTeam, name="registrationTeam"),
    path('create_delegation/', views.createAdvisor, name="createMyDelegation"),
    path('advisor/<int:advisor_id>/', views.displayAdvisor, name="displayMyDelegation"),
]