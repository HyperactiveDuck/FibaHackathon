from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('transactions/', views.transactions, name='transactions'),
    path('budgets/', views.budgets, name='budgets'),
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.settings, name='settings'),
]