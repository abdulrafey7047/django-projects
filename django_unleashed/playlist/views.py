from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User

from .forms import Signup, Login, Edit
from .models import Song, Playlist


def home(request):
    playlists = Playlist.objects.all()
    return render(request, 'playlist/home.html', {"my_playlists": playlists})


def about(request):
    return render(request, 'playlist/about.html')


def playlist(request, id):

    songs = []
    playlist = get_object_or_404(Playlist, pk=id)
    all_songs = Song.objects.all()

    for song in all_songs:
        if id == song.playlist_id:
            songs.append(song)

    return render(request,
                  'playlist/songs.html',
                  {"songs": songs, "playlist_name": playlist.name})


def edit(request, id):

    form = Edit(request.POST or None)
    if form.is_valid():
        track = form.cleaned_data.get("track")
        album = form.cleaned_data.get("album")
        artist = form.cleaned_data.get("artist")
        length = form.cleaned_data.get("length")
        playlist_id = form.cleaned_data.get("playlist_id")

        song = Song.objects.get(id=id)

        song.track = track
        song.album = album
        song.artist = artist
        song.length = length
        song.playlist_id = playlist_id

        song.save()

        return render(
                      request,
                      'playlist/edit.html',
                      {
                        "form": form,
                        "status": "Your song is updated successfully!"
                      }
                     )

    return render(request, 'playlist/edit.html', {"form": form})


def signup(request):

    form = Signup(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        name = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        if password != confirm_password:
            return render(
                          request,
                          'playlist/signup.html',
                          {
                            "form": form,
                            "status": "Your passwords don't match!"
                          }
                         )
        else:
            try:
                _ = User.objects.get(email=email)
                return render(
                              request,
                              'playlist/signup.html',
                              {
                                "form": form,
                                "status": "This email already exists in the \
                                           system! Please log in instead."
                              }
                            )
            except Exception as e:
                print(e)
                new_user = User.objects.create_user(
                    username=name, email=email, password=password)
                new_user.save()
                return render(
                              request,
                              'playlist/signup.html',
                              {
                                "form": form,
                                "status": "Signed up Successfully!"
                              }
                             )

    return render(request, 'playlist/signup.html', {"form": form})


def login(request):

    form = Login(request.POST or None)
    status = " "
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            status = "You have successfully logged in!"
        else:
            status = "You credentials are not valid. Try again!"
    return render(request,
                  'playlist/login.html',
                  {"form": form, "status": status})


def logout(request):

    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('home')
