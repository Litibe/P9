"""Review_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.views import LoginView, PasswordChangeView
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', LoginView.as_view(template_name='authentication/connexion.html',
         redirect_authenticated_user=True), name='connexion'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='authentication/password_change.html',
        success_url='done/'), name='password_change'),
    path('password_change/done/', views.password_changed,
         name='password_change_done'),
    path("inscription/", views.inscription, name="inscription"),
    path("user_picture/", views.user_picture, name="user_picture"),
    path('deconnexion/', views.deconnexion, name="deconnexion"),
]
