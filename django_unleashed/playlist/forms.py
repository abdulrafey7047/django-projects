from django import forms
from .models import Song


class Signup(forms.Form):
    username = forms.CharField(required=True, max_length=70)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, min_length=5)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, required=True, min_length=5)


class Login(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, min_length=5)


class Edit(forms.ModelForm):

    class Meta:
        model = Song
        fields = ["track", "album", "artist", "length", "playlist_id"]
        exclude = []
