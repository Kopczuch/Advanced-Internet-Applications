import os
import json
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movielens.settings')
# Initialize Django
django.setup()

from django.contrib.auth.hashers import make_password
from userview.models import Movie, Image, Genre, Comment, Rating
from django.contrib.auth.models import User
from django.core.files import File

with open('fixtures/picked_comments.json', 'r') as file:
    comments_data = json.load(file)

for comment_data in comments_data:
    # Find the associated Movie and User models
    try:
        movie = Movie.objects.get(pk=comment_data['movie'])
        user = User.objects.get(pk=comment_data['user'])
    except (Movie.DoesNotExist, User.DoesNotExist):
        continue

    # Create Comment model instance
    comment = Comment()
    comment.movie = movie
    comment.user = user
    comment.comment = comment_data['comment']
    comment.timestamp = comment_data['timestamp']

    # Save the comment model to the database
    comment.save()