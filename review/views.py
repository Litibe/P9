import os

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from . import forms, models
from authentication import models as auth_models


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
    context = {'form': form}
    return render(request, 'review/create_new_ticket.html', context)


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
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = models.Ticket.objects.get(id=number_ticket)
            review.user = request.user
            review.save()
            return redirect('review:flux')
    context = {'form': form, "tickets": tickets}
    return render(request, 'review/create_new_review.html', context)


@login_required
def create_new_review(request):
    return render(request, 'review/create_new_review.html')


@login_required
def follow(request):
    all_followed_id = list(models.UserFollows.objects.filter(
        user=request.user.id).values_list('followed_user_id', flat=True))
    all_followed_id.append(request.user.id)
    all_users_to_be_followed = auth_models.User.objects.all().exclude(
        id__in=all_followed_id)
    user_form = forms.UserFollowsForm()
    remove_user_followed_form = forms.UserRemoveFollowsForm()
    user_followed_by_request_user = models.UserFollows.objects.filter(
        user=request.user.id)
    request_user_followed_by_other = models.UserFollows.objects.filter(
        followed_user=request.user.id)
    context = {"user_form": user_form, "remove_user_followed_form": remove_user_followed_form, "all_users_to_be_followed": all_users_to_be_followed,
               "user_followed_by_request_user": user_followed_by_request_user, "request_user_followed_by_other": request_user_followed_by_other}

    if request.method == 'POST':
        user_form = forms.UserFollowsForm(request.POST)
        remove_user_followed_form = forms.UserRemoveFollowsForm(request.POST)
        if user_form.is_valid():
            follow = models.UserFollows.objects.filter(
                user_id=request.user.id, followed_user=request.POST.get("user")[0])
            if not follow:
                follow = models.UserFollows.objects.create()
                follow.user_id = request.user.id
                follow.followed_user_id = str(request.POST.get("user")[0])
                follow.save()

        if request.POST.get("user_followed_to_delete"):
            followed = models.UserFollows.objects.filter(
                user_id=request.user.id, followed_user=request.POST.get("user_followed_to_delete")[0])
            followed.delete()
        return redirect("review:follow")
    return render(request, 'review/follow.html', context)


@ login_required
def flux(request):
    all_followed = models.UserFollows.objects.filter(
        user_id=request.user.id).values_list('followed_user_id', flat=True)
    all_followed = list(all_followed)
    all_followed.append(request.user.id)

    reviews = models.Review.objects.filter(
        user_id__in=all_followed).values()
    reviews_link_tickets = models.Review.objects.filter(
        user_id__in=all_followed).values_list('ticket_id', flat=True)
    tickets = models.Ticket.objects.filter(
        user_id__in=all_followed) | models.Ticket.objects.filter(id__in=reviews_link_tickets)
    tickets = tickets.order_by("-id")
    context = {"tickets": tickets, "reviews": reviews,
               "reviews_link_tickets": reviews_link_tickets}
    return render(request, 'review/flux.html', context=context)


@ login_required
def posts(request):
    reviews = models.Review.objects.filter(
        user_id=request.user.id).values()
    reviews_link_tickets = models.Review.objects.filter(
        user_id=request.user.id).values_list('ticket_id', flat=True)
    tickets = models.Ticket.objects.filter(
        user_id=request.user.id) | models.Ticket.objects.filter(id__in=reviews_link_tickets)
    tickets = tickets.order_by("-id")
    context = {"tickets": tickets, "reviews": reviews,
               "reviews_link_tickets": reviews_link_tickets}
    return render(request, 'review/posts.html', context)
# GESTION TICKETS


@ login_required
def modify_ticket(request, number_ticket):
    context = {"number_ticket": number_ticket}
    tickets = get_object_or_404(models.Ticket, id=number_ticket)
    if request.user.id == tickets.user_id:
        form = forms.ModifTicketTitleDescription(instance=tickets)
        context["form"] = form
        picture = forms.ModifPicture(instance=tickets)
        context["picture"] = picture
        context["tickets"] = tickets
        if request.method == 'POST':
            form = forms.ModifTicketTitleDescription(
                request.POST)
            tickets.title = request.POST.get("title", "")
            tickets.description = request.POST.get("description", "")
            tickets.save()

            picture = forms.ModifPicture(request.POST, request.FILES)
            if all([picture.is_valid()]):
                new_picture = picture.save(commit=False)
                tickets.image = new_picture.image
                tickets.save()
            return redirect('review:posts')

    return render(request, 'review/modify_ticket.html', context)


@ login_required
def read_ticket(request, number_ticket):
    ticket = get_object_or_404(models.Ticket, id=number_ticket)
    context = {"ticket": ticket, "number_ticket": number_ticket}
    review = models.Review.objects.filter(ticket_id=number_ticket)
    if review:
        ticket.review = review[0]
        context["review"] = review[0]
    return render(request, 'review/read_ticket.html', context)


@ login_required
def delete_ticket(request, number_ticket):
    context = {"number_ticket": number_ticket}
    ticket = get_object_or_404(models.Ticket, id=number_ticket)
    if ticket:
        context["ticket"] = ticket
    review = models.Review.objects.filter(ticket_id=number_ticket)
    if review:
        ticket.review = review[0]
        context["review"] = review

    if request.method == 'POST':
        ticket = get_object_or_404(
            models.Ticket, id=number_ticket)
        if ticket:
            ticket.delete()
        return redirect("review:posts")
    return render(request, 'review/delete_ticket.html', context)


# GESTION REVIEW


@ login_required
def modify_review(request, number_review):
    context = {"number_review": number_review}
    reviews = get_object_or_404(models.Review, id=number_review)
    ticket = get_object_or_404(models.Ticket, id=reviews.ticket_id)
    if request.user.id == reviews.user_id:
        form = forms.ReviewForm(instance=reviews)
        if request.method == 'POST':
            form = forms.ReviewForm(
                request.POST, instance=reviews)
            if form.is_valid():
                review = form.save(commit=False)
                review.save()
                return redirect('review:flux')
        context["form"] = form
        if ticket:
            context["ticket"] = ticket
        if reviews:
            context["reviews"] = reviews

    return render(request, 'review/modify_review.html', context)


@ login_required
def delete_review(request, number_review):
    review = get_object_or_404(models.Review, id=number_review)
    ticket = get_object_or_404(models.Ticket, id=review.ticket_id)
    ticket.review = review
    if request.method == 'POST':
        review = get_object_or_404(models.Review, id=number_review)
        review.delete()
        return redirect("review:posts")
    context = {"review": review, "ticket": ticket}
    return render(request, 'review/delete_review.html', context)
