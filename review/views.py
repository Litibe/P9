from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from . import forms
from . import models
from django.contrib.auth.models import User

import review


@login_required
def create_new_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('review:flux')
    return render(request, 'review/create_new_ticket.html', context={'form': form})


@login_required
def create_new_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket_id = ticket.id
            review.user = request.user
            review.save()
            return redirect('review:flux')
    context = {'ticket_form': ticket_form, "review_form": review_form}
    return render(request, 'review/create_new_ticket_and_review.html', context)


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
    tickets = get_object_or_404(models.Ticket, id=number_ticket)
    reviews = get_object_or_404(
        models.Review, ticket_id=number_ticket)
    return render(request, 'review/read_ticket.html', context={"tickets": tickets, "reviews": reviews})


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
    tickets = [ticket for ticket in tickets]
    for ticket in tickets:
        for review in reviews:
            if review.ticket_id == ticket.id:
                ticket.review = review

    return render(request, 'review/flux.html', context={"tickets": tickets, "reviews": reviews})


@login_required
def posts(request):
    return render(request, 'review/posts.html')


@login_required
def read_ticket(request, number_ticket):
    tickets = models.Ticket.objects.filter(id=number_ticket)
    return render(request, 'review/read_ticket.html', context={"tickets": tickets})
