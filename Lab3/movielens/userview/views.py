# from django.shortcuts import render, get_object_or_404
# from django.http import HttpRequest, HttpResponse
# from django.template import loader
# from .models import Movie, Genre
# def index(request : HttpRequest):
#     movies = Movie.objects.order_by('-title')
#     template = loader.get_template('userview/index.html')
#     context = {
#     'movies' : movies
#     }
#     return HttpResponse(template.render(context,request))
# def view_movie(request: HttpRequest, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
#     return render(request, 'userview/movie.html', {'movie': movie})
# def view_genre(request: HttpRequest, genre_id):
#     genre = get_object_or_404(Genre, id=genre_id)
#     movies = Movie.objects.filter(genres=genre)
#     return render(request, 'userview/genre.html', {'genre': genre, 'movies': movies})

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.db.models import Avg, IntegerField, Q
from django.db.models.functions import Coalesce
from userview.forms import *
from .models import Movie, Genre, Rating, Comment, Image
from django.shortcuts import get_object_or_404

class IndexView(generic.ListView):
    template_name = 'userview/index.html'
    context_object_name = 'movies'
    paginate_by = 2
    model = Movie
    def get_queryset(self):
        return Movie.objects.order_by('-title')
    
class MovieView(generic.DetailView):
    model = Movie
    template_name = 'userview/movie.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        comments = Comment.objects.filter(movie=movie)
        context['comments'] = comments
        avg_rating = Rating.objects.filter(movie=movie).aggregate(
            average_rating=Coalesce(Avg('value', output_field=IntegerField()), 0)
        )['average_rating']
        context['avg_rating'] = avg_rating
        gallery = Image.objects.filter(movie=movie)
        context['gallery'] = gallery.order_by('-front_image')
        if self.request.user.is_authenticated and Rating.objects.filter(movie=movie, user=self.request.user).first() != None:
            user_rating = Rating.objects.filter(movie=movie, user=self.request.user).first().value
        else:
            user_rating = 0
        context['user_rating'] = user_rating
        context['comment_form'] = CommentForm()
        return context
    
class GenreView(generic.DetailView):
    model = Genre
    template_name = 'userview/genre.html'
    
class RatingView(generic.DeleteView):
    model = Rating
    template_name = 'userview/rating.html'
        
class CommentView(generic.DetailView):
    model = Comment
    template_name = 'userview/comment.html'

from django.db.models import Avg

def search(request):
    search_results = None

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            genres = search_form.cleaned_data['genres'].split(' ')
            title = search_form.cleaned_data['title']
            min_rating = search_form.cleaned_data['min_rating']
            query = Q()
            if genres:
                for genre in genres:
                    query |= Q(genres__name__icontains=genre.strip().lower())
            if title:
                query &= Q(title=title)
            if min_rating:
                query &= Q(rating__gte=min_rating)
            search_results = Movie.objects.filter(query).annotate(avg_rating=Avg('rating__value')).order_by('title')
        else:
            search_form = SearchForm()
    else:
        search_form = SearchForm()

    context = {'search_form': search_form, 'search_results': search_results}
    return render(request, 'userview/search.html', context)


def register_request(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render (request=request, template_name="userview/register.html",
        context={"register_form":form})
    

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, 'userview/login.html', {'login_form': form})


def logout_request(request):
    logout(request)
    return redirect('/')


def my_ratings(request):
    if request.user.is_authenticated:
        user_ratings = Rating.objects.filter(user=request.user)
        return render(request=request, template_name='userview/my_ratings.html',
                  context={"user_ratings":user_ratings})
    return redirect("/my_ratings")


def new_rating(request, movie_id=None):
    if request.method == 'POST':
        add_form = RatingForm(request.POST)
        if add_form.is_valid():
            rating = add_form.save(commit=False)
            rating.user = request.user
            if movie_id:
                movie = get_object_or_404(Movie, id=movie_id)
                rating.movie = movie
            rating.save()
            return redirect('my_ratings')
    else:
        initial = {}
        if movie_id:
            initial['movie'] = movie_id
            add_form = RatingForm(initial=initial, disable_movie=True)
        else:
            add_form = RatingForm(initial=initial)

    context = {'add_form': add_form}
    return render(request, 'userview/new_rating.html', context)


def movie_gallery(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    gallery = Image.objects.filter(movie=movie)
    context = {
        'movie': movie,
        'gallery': gallery,
    }
    return render(request, template_name='userview/gallery.html', context=context)


def add_comment(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()
            return redirect('/movie/' + str(movie.id))
    else:
        comment_form = CommentForm()
    context = {'comment_form': comment_form, 'movie': movie}
    return render(request, 'userview/add_comment.html', context)


    