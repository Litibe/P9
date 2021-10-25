from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from . import forms
from . import models
from django.contrib.auth.models import User


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
def create_new_review_for_ticket(request, number_ticket):
    tickets = models.Ticket.objects.filter(id=number_ticket)
    print(tickets)
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = models.Ticket.objects.get(id=number_ticket)
            review.user = request.user
            # now we can save
            review.save()
            return redirect('review:flux')
    return render(request, 'review/create_new_review.html', context={'form': form, "tickets": tickets})


@login_required
def read_ticket(request, number_ticket):
    print(number_ticket)
    tickets = models.Ticket.objects.filter(id=number_ticket)
    return render(request, 'review/read_ticket.html', context={"tickets": tickets})


@login_required
def create_new_review(request):
    return render(request, 'review/create_new_ticket.html')


@login_required
def home(request):
    return render(request, 'review/home.html')


@login_required
def flux(request):
    tickets = models.Ticket.objects.all().order_by('-time_created')
    reviews = models.Review.objects.all().order_by('-time_created')
    print(reviews)
    return render(request, 'review/flux.html', context={"tickets": tickets, "reviews": reviews})


@login_required
def posts(request):
    return render(request, 'review/posts.html')


@login_required
def read_ticket(request, number_ticket):
    tickets = models.Ticket.objects.filter(id=number_ticket)
    return render(request, 'review/read_ticket.html', context={"tickets": tickets})