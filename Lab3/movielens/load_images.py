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

movies_dir = 'fixtures/picked_movies'

# Step 4: Read and Load Image Data
for filename in os.listdir(movies_dir):
    if filename.endswith('.jpg'):
        # Extract movie ID from the file name
        movie_id = filename.split('.')[0]

        # Find the associated Movie model
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            print(f"Movie with ID {movie_id} does not exist.")
            continue

        # Create Image model instance
        image = Image()
        image.movie = movie
        image.title = movie.title
        image.front_image = True
        # Set the image file
        file_path = os.path.join(movies_dir, filename)
        with open(file_path, 'rb') as f:
            django_file = File(f)
            image.img.save(filename, django_file, save=True)

        # Save the image model to the database
        image.save()