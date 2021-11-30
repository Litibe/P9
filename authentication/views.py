from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . import users_form


def deconnexion(request):
    logout(request)
    return redirect('authentication:connexion')


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
    context = {"form": form, "message": message, "color": color}
    return render(request, 'authentication/connexion.html', context)


def inscription(request):
    form = users_form.SignupForm()
    if request.method == 'POST':
        form = users_form.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("review:home")
    context = {'form': form}
    return render(request, 'authentication/inscription.html', context)


@login_required
def user_picture(request):
    form = users_form.UserPictureForm(instance=request.user)
    if request.method == 'POST':
        form = users_form.UserPictureForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('review:flux')
    context = {'form': form}
    return render(request, 'authentication/user_picture.html', context)


def password_changed(request):
    return render(request, 'authentication/password_change_done.html',)
