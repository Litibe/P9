from django import forms

from django.db import models
from . import models as models_review


class TicketForm(forms.ModelForm):
    class Meta:
        model = models_review.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models_review.Review
        fields = ["headline", 'rating', 'body']


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = models_review.UserFollows
        fields = ["user"]


class UserRemoveFollowsForm(forms.ModelForm):
    class Meta:
        model = models_review.UserFollows
        fields = ["user"]
