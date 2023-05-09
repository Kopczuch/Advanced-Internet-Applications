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

from django.views import generic
from .models import Movie, Genre
class IndexView(generic.ListView):
    template_name = 'userview/index.html'
    context_object_name = 'movies'
    paginate_by = 1
    model = Movie
    def get_queryset(self):
        return Movie.objects.order_by('-title')
class MovieView(generic.DetailView):
    model = Movie
    template_name = 'userview/movie.html'
class GenreView(generic.DetailView):
    model = Genre
    template_name = 'userview/genre.html'