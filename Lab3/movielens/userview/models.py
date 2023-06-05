from django.db import models
from django.conf import settings
from django.db.models import Q, Max, Avg
from embed_video.fields import EmbedVideoField

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=1000)
    year = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    director = models.CharField(max_length=1000)
    imdblink = models.URLField(max_length=500)
    description = models.TextField()

    def __str__(self):
        return self.title
    
    def get_most_liked_movies():
        latest_rating_ids = Rating.objects.values('movie').annotate(max_id=Max('id')).order_by('-max_id')
        movie_ids = [rating['movie'] for rating in latest_rating_ids]
        most_liked_movies = Movie.objects.filter(id__in=movie_ids).annotate(avg_rating=Avg('rating__value')).filter(avg_rating__gte=4).order_by('-avg_rating')
        return most_liked_movies
    
    def similar_movies(self):
        similar_movies = Movie.objects.filter(Q(director=self.director) | Q(genres__in=self.genres.all())).exclude(id=self.id).distinct()
        return list(similar_movies)





class Rating(models.Model):
    value = models.FloatField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rating {self.rating} for {self.movie}"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.IntegerField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.movie}"

class Image(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images/')
    front_image = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    
class EmbeddedVideoItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    video = EmbedVideoField()
    class Meta:
        ordering = ['title']