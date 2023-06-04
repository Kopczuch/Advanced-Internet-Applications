from django.db import models
from django.conf import settings
from embed_video.fields import EmbedVideoField

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=1000)
    genres = models.ManyToManyField(Genre)
    imdbLink = models.URLField(max_length=500)
    description = models.TextField()

    def __str__(self):
        return self.title

class Rating(models.Model):
    rating = models.FloatField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rating {self.rating} for {self.movie}"

class Comment(models.Model):
    comment = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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