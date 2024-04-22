from django.forms import ModelForm
from django import forms
from .models import BookClub, Type, BookFormat, Shelf, Reading, Question, Response


class CreateClubForm(ModelForm):
    club_name = forms.CharField(label="Book Club Name", max_length=64)
    types = forms.ModelMultipleChoiceField(
        label='Select Club Types (Up to 3)', queryset=Type.objects.all())
    club_description = forms.CharField(
        label="Club Description", max_length=500, widget=forms.Textarea(attrs={"rows": 3, "cols": 20}))

    class Meta:
        model = BookClub
        fields = ["club_name", "types", "club_description"]


class SearchBookForm(forms.Form):
    book_name = forms.CharField(
        label="Book Name", max_length=150)
    author_name = forms.CharField(
        label="Author Name", max_length=100, required=False)


class AddToShelfForm(ModelForm):
    cover_edition_key = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'cover_edition_key'}), max_length=64)
    book_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'book_name', 'readonly': 'true'}), max_length=200)
    publish_year = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'publish_year'}), max_length=4)
    author = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'author'}), max_length=100)
    format = forms.ModelChoiceField(
        label='Select Book Format', queryset=BookFormat.objects.all(), required=True)

    class Meta:
        model = Shelf
        fields = ["cover_edition_key", "book_name",
                  "publish_year", "author", "format"]


class ManageClubForm(ModelForm):
    club_id = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'club_id'}), max_length=64)
    cover_edition_key = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'cover_edition_key'}), max_length=64)
    book_name = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'book_name'}), max_length=200)
    publish_year = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'publish_year'}), max_length=4)
    author = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'author'}), max_length=100)

    class Meta:
        model = Reading
        fields = ["cover_edition_key", "book_name",
                  "publish_year", "author"]


class QuestionForm(ModelForm):
    description = forms.CharField(
        label="Enter Your Question Here:", max_length=500, widget=forms.Textarea(attrs={"rows": 2, "cols": 40}))

    class Meta:
        model = Question
        fields = ["description"]


class ResponseForm(ModelForm):
    description = forms.CharField(
        label="Your Response:", max_length=500, widget=forms.Textarea(attrs={"rows": 2, "cols": 40}))

    class Meta:
        model = Response
        fields = ["description"]
