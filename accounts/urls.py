from django.urls import path
from . import views

#different options once logged in
urlpatterns = [        
    path('logout/', views.logoutAccount, name='logout'),
    path('login/', views.loginAccount, name='login'),
    path('changepwd/', views.changePassword, name='changepwd'),
    path('pwdChanged/', views.passwordChanged, name='pwdChanged'),
]
