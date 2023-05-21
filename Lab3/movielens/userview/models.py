from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name
class Movie(models.Model):
    title = models.CharField(max_length=1000)
    genres = models.ManyToManyField(Genre)
    imdblink = models.URLField(max_length=500)
    def __str__(self):
        return self.title
class Rating(models.Model):
    value = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.movie.title
class Comment(models.Model):
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
class Image(models.Model):
    title = models.CharField(max_length = 100)
    img = models.ImageField(upload_to='images/')
    front_image = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def __str__(self):
        return self.title