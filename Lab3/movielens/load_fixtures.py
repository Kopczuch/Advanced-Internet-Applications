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

# Step 3: Read and Load Movie Data
movies_dir = 'fixtures/picked_movies'

for filename in os.listdir(movies_dir):
    if filename.endswith('.json'):
        # Read JSON file
        with open(os.path.join(movies_dir, filename), 'r') as file:
            movie_data = json.load(file)

        # Create Movie model instance
        movie = Movie()
        # Set movie attributes excluding the 'image' field
        movie.title = movie_data['title']
        movie.year = movie_data['year']
        movie.director = movie_data['director']
        movie.imdblink = movie_data['imdbLink']
        movie.description = movie_data['description']

        # Split genre names by comma and create Genre instances
        genre_names = movie_data['genre'].split(',')
        genres = []
        for genre_name in genre_names:
            genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
            genres.append(genre)

        # Save the movie model to the database
        movie.save()
        # Assign genres to the movie
        movie.genres.set(genres)

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

# Step 5: Read and Load User Data
users_dir = 'fixtures/picked_users'

for filename in os.listdir(users_dir):
    if filename.endswith('.json'):
        # Extract the username from the file name (assuming the file name format is 'username.json')
        username = filename.split('.')[0]
        
        # Check if the user already exists in the database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Create a new user object
            user = User(username=username)
        
        # Load the user data from the JSON file
        file_path = os.path.join(users_dir, filename)
        with open(file_path, 'r') as f:
            user_data = json.load(f)
        
        if user_data['user_id'] == "9999":
            user = User.objects.create_superuser(
                id=9999,
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password']
            )
            
        else:
            # Set the user's hashed password
            password = user_data['password']
            hashed_password = make_password(password)
            user.password = hashed_password
            user.id = user_data['user_id']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.username = user_data['username']
        
        # Save the user object to the database
        user.save()
        
# Step 6: Read and Load Comment Data
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

# Step 7: Read and Load Rating Data
with open('fixtures/picked_ratings.json', 'r') as file:
    ratings_data = json.load(file)

for rating_data in ratings_data:
    # Find the associated Movie and User models
    try:
        movie = Movie.objects.get(pk=rating_data['movie_id'])
        user = User.objects.get(pk=rating_data['user_id'])
    except (Movie.DoesNotExist, User.DoesNotExist):
        continue

    # Create Rating model instance
    rating = Rating()
    rating.movie = movie
    rating.user = user
    rating.value = rating_data['rating']

    # Save the rating model to the database
    rating.save()
