import os
import json
import django
from django.core.management import call_command
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movielens.settings')
django.setup()

# Import necessary models
from userview.models import Genre, Movie, Image
from django.contrib.auth.models import User

def create_fixture_files():
    # Get the directory path of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the fixture file names
    fixture_files = [
        'genres.json',
        'movies.json',
        'images.json',
        'comments.json',
        'ratings.json',
    ]

    # Create empty fixture files if they don't exist
    for file in fixture_files:
        file_path = os.path.join(script_dir, 'fixtures', file)
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

def load_fixtures():
    # Load genres fixture
    genres_fixture = os.path.join('fixtures', 'genres.json')
    call_command('loaddata', genres_fixture)

    # Load movies and images
    movies_dir = os.path.join('fixtures', 'picked_movies')
    movies_data = []
    images_data = []

    for filename in os.listdir(movies_dir):
        if filename.endswith('.json'):
            movie_file = os.path.join(movies_dir, filename)
            with open(movie_file, 'r') as file:
                movie_data = json.load(file)
                movies_data.append(movie_data)

                image_filename = movie_data['image']
                image_data = {
                    'model': 'userview.image',
                    'fields': {
                        'title': movie_data['title'],
                        'img': os.path.join('picked_movies', image_filename),
                        'front_image': True,
                        'movie': None,
                    }
                }
                images_data.append(image_data)

    # Load user data
    users_dir = os.path.join('fixtures', 'picked_users')
    users_data = []

    for filename in os.listdir(users_dir):
        if filename.endswith('.json'):
            user_file = os.path.join(users_dir, filename)
            with open(user_file, 'r') as file:
                user_data = json.load(file)
                users_data.append(user_data)

    # Load comments
    comments_file = os.path.join('fixtures', 'picked_comments.json')
    with open(comments_file, 'r') as file:
        comments_data = json.load(file)

    # Load ratings
    ratings_file = os.path.join('fixtures', 'picked_ratings.json')
    with open(ratings_file, 'r') as file:
        ratings_data = json.load(file)

    # Create the fixture data
    fixture_data = movies_data + images_data + users_data + comments_data + ratings_data

    # Write the fixture data to a file
    fixture_file = os.path.join('fixtures', 'all_data.json')
    with open(fixture_file, 'w') as file:
        json.dump(fixture_data, file)

    # Load the combined fixture into the database
    call_command('loaddata', fixture_file)

# Execute the script
if __name__ == "__main__":
    create_fixture_files()
    load_fixtures()
