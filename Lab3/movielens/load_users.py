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