from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from . import forms
from . import models
from authentication import models as auth_models

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
def create_new_review(request):
    return render(request, 'review/create_new_review.html')


@login_required
def follow(request):
    all_followed = models.UserFollows.objects.filter(user=request.user.id)
    all_followed_id = [followed.followed_user_id for followed in all_followed]
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
            user_form.save(commit=False)
            try:
                follow = models.UserFollows.objects.filter(
                    user_id=request.user.id, followed_user=request.POST.get("user")[0])
                if not follow:
                    follow = models.UserFollows.objects.create()
                    follow.user_id = request.user.id
                    follow.followed_user_id = str(request.POST.get("user")[0])
                    follow.save()
            except:
                pass
        if request.POST.get("user_followed_to_delete"):
            try:

                followed = models.UserFollows.objects.filter(
                    user_id=request.user.id, followed_user=request.POST.get("user_followed_to_delete")[0])
                followed.delete()
            except:
                pass
        return redirect("review:follow")
    return render(request, 'review/follow.html', context=context)


@ login_required
def flux(request):
    all_followed = models.UserFollows.objects.filter(user=request.user.id)
    all_followed_id = [followed.followed_user_id for followed in all_followed]
    all_followed_id.append(request.user.id)

    all_tickets = models.Ticket.objects.all().order_by('-time_created')
    tickets = models.Ticket.objects.all().order_by(
        '-time_created').filter(user_id__in=all_followed_id)
    reviews = models.Review.objects.all().order_by(
        '-time_created').filter(user_id__in=all_followed_id)
    all_ticket = [ticket for ticket in tickets]
    for ticket in all_tickets:
        for review in reviews:
            if review.user_id not in all_followed_id:
                pass
            else:
                if review.ticket_id == ticket.id:
                    ticket.review = review
                    all_ticket.append(ticket)
                    print("append")
    all_ticket_id = [ticket.id for ticket in all_ticket]
    all_ticket_id.sort()
    all_tickets = models.Ticket.objects.filter(
        id__in=all_ticket_id).order_by('-time_created')
    all_ticket = [ticket for ticket in all_tickets]
    for ticket in all_ticket:
        for review in reviews:
            if review.ticket_id == ticket.id:
                ticket.review = review
    return render(request, 'review/flux.html', context={"tickets": all_ticket, "reviews": reviews})


@ login_required
def posts(request):
    my_tickets = models.Ticket.objects.filter(
        user_id=request.user.id).order_by('-time_created')

    tickets = models.Ticket.objects.all().order_by('-time_created')
    reviews = models.Review.objects.filter(
        user_id=request.user.id).order_by('-time_created')
    tickets = [ticket for ticket in tickets]
    for ticket in tickets:
        for review in reviews:
            if review.ticket_id == ticket.id:
                ticket.review = review

    return render(request, 'review/posts.html', context={"tickets": tickets, "reviews": reviews, "my_tickets": my_tickets})
# GESTION TICKETS


@ login_required
def modify_ticket(request, number_ticket):
    context = {"number_ticket": number_ticket}
    tickets = get_object_or_404(models.Ticket, id=number_ticket)
    if request.user.id == tickets.user_id:
        form = forms.TicketForm()
        context["form"] = form
        picture = forms.ModifPicture(instance=tickets)
        context["picture"] = picture
        context["tickets"] = tickets
        if request.method == 'POST':
            tickets.title = request.POST.get("title", "")
            tickets.description = request.POST.get("description", "")
            tickets.save()

            picture = forms.ModifPicture(request.POST, request.FILES)
            if all([picture.is_valid()]):
                picture.save()
            return redirect('review:posts')

    return render(request, 'review/modify_ticket.html', context=context)


@ login_required
def read_ticket(request, number_ticket):
    try:
        ticket = get_object_or_404(models.Ticket, id=number_ticket)
        context = {"ticket": ticket, "number_ticket": number_ticket}
        try:
            review = get_object_or_404(
                models.Review, ticket_id=number_ticket)
            ticket.review = review
            context = {"ticket": ticket,
                       "number_ticket": number_ticket, "review": review}
        except:
            pass
    except:
        context = {"number_ticket": number_ticket}

    return render(request, 'review/read_ticket.html', context=context)


@ login_required
def delete_ticket(request, number_ticket):
    try:
        ticket = get_object_or_404(models.Ticket, id=number_ticket)
        context = {"ticket": ticket, "number_ticket": number_ticket}
        try:
            review = get_object_or_404(
                models.Review, ticket_id=number_ticket)
            ticket.review = review
            context = {"ticket": ticket,
                       "number_ticket": number_ticket, "review": review}
        except:
            pass
    except:
        context = {"number_ticket": number_ticket}
    if request.method == 'POST':
        try:
            review = get_object_or_404(models.Review, ticket_id=number_ticket)
            review.delete()
        except:
            pass
        ticket = get_object_or_404(
            models.Ticket, id=number_ticket)
        ticket.delete()
        return redirect("review:posts")
    return render(request, 'review/delete_ticket.html', context=context)


# GESTION REVIEW


@ login_required
def modify_review(request, number_review):
    reviews = get_object_or_404(models.Review, id=number_review)
    ticket = get_object_or_404(models.Ticket, id=reviews.ticket_id)
    if request.user.id == reviews.user_id:
        form = forms.ReviewForm(instance=reviews)
        if request.method == 'POST':
            form = forms.ReviewForm(
                request.POST, request.FILES, instance=reviews)
            if form.is_valid():
                review = form.save(commit=False)
                review.save()
                return redirect('review:flux')
        context = {"form": form, "reviews": reviews,
                   "number_review": number_review, "ticket": ticket}
    else:
        context = {"number_review": number_review}

    return render(request, 'review/modify_review.html', context=context)


@ login_required
def delete_review(request, number_review):
    review = get_object_or_404(models.Review, id=number_review)
    ticket = get_object_or_404(models.Ticket, id=review.ticket_id)
    ticket.review = review
    if request.method == 'POST':
        review = get_object_or_404(models.Review, id=number_review)
        review.delete()
        return redirect("review:posts")
    return render(request, 'review/delete_review.html', context={"review": review, "ticket": ticket})
