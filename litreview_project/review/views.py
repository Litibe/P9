from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from . import forms
from . import models


@login_required
def create_new_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect('review:flux')
    return render(request, 'review/create_new_ticket.html', context={'form': form})


@login_required
def create_new_review(request):
    return render(request, 'review/create_new_ticket.html')


@login_required
def home(request):
    return render(request, 'review/home.html')


@login_required
def flux(request):
    tickets = models.Ticket.objects.all()

    return render(request, 'review/flux.html', context={"tickets": tickets})


@login_required
def posts(request):
    return render(request, 'review/posts.html')
