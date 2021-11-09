from django import forms

from django.db import models
from . import models as models_review


class TicketForm(forms.ModelForm):
    title = forms.CharField(label="Titre", widget=forms.TextInput(
        {"class": "form-control", "placeholder": "Mettez le titre du livre"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(
        {"class": "form-control", "placeholder": "Mettez le titre du livre"}))

    class Meta:
        model = models_review.Ticket
        fields = ['title', 'description', 'image']


class ModifTicketTitleDescription(forms.ModelForm):
    title = forms.CharField(label="Titre", widget=forms.TextInput(
        {"class": "form-control", "placeholder": "Mettez le titre du livre"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(
        {"class": "form-control", "placeholder": "Mettez le titre du livre"}))

    class Meta:
        model = models_review.Ticket
        fields = ['title', 'description']


class ModifPicture(forms.ModelForm):

    class Meta:
        model = models_review.Ticket
        fields = ['image']


class ReviewForm(forms.ModelForm):

    headline = forms.CharField(label="Titre de la critique", widget=forms.TextInput(
        {"class": "form-control", "placeholder": "Mettez le titre de votre critique"}))

    rating = forms.CharField(label="Votre note", widget=forms.NumberInput(
        {"class": "form-check", "min": "0", "max": "5", "step": "1"}))
    body = forms.CharField(label="Votre critique", widget=forms.Textarea(
        {"class": "form-control", "placeholder": "Mettez le détails de votre critique"}))

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
