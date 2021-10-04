from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import users_form


@login_required
def home(request):
    return render(request, 'review/home.html')


def deconnexion(request):
    logout(request)
    return redirect('review:connexion')


def connexion(request):
    form = users_form.LoginForm()
    message = ''
    color = ""
    if request.method == 'POST':
        form = users_form.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect("review:home")
            else:
                message = 'Identifiants invalides !'
                color = "text-danger"
    return render(request, 'review/connexion.html', context={"form": form, "message": message, "color": color})


def inscription(request):
    form = users_form.SignupForm()
    if request.method == 'POST':
        form = users_form.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("review:home")
    return render(request, 'review/inscription.html', context={'form': form})
