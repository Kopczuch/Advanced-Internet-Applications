from django.core.management import call_command
from django.conf import settings
import os
import json
from userview.models import Movie, Genre, Comment, Rating, Image
from django.contrib.auth.models import User


def load_fixtures():
    fixture_dir = os.path.join(settings.BASE_DIR, 'movielens', 'fixtures')
    fixtures = [
        'genres.json',
        'movies.json',
        'users.json',
        'comments.json',
        'ratings.json'
    ]

    for fixture in fixtures:
        fixture_file = os.path.join(fixture_dir, fixture)
        with open(fixture_file, 'r') as file:
            fixture_data = json.load(file)

        model_name = fixture_data[0]['model']

        if model_name == 'movielens.movie':
            for item in fixture_data:
                fields = item['fields']
                genres = fields.pop('genres', None)
                if genres:
                    genre_objects = []
                    for genre_name in genres.split(', '):
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        genre_objects.append(genre)
                    fields['genres'] = genre_objects
                fields['imdblink'] = fields.pop('imdbLink')
                movie = Movie.objects.create(**fields)
                image_file = fields.pop('image', None)
                if image_file:
                    Image.objects.create(title=fields['title'], img=f'picked_movies/{image_file}', front_image=True,
                                         movie=movie)

        elif model_name == 'movielens.rating':
            for item in fixture_data:
                fields = item['fields']
                fields['user'] = User.objects.get(id=fields.pop('user_id'))
                fields['movie'] = Movie.objects.get(id=fields.pop('movie_id'))
                fields['value'] = fields.pop('rating')
                Rating.objects.create(**fields)

        elif model_name == 'movielens.comment':
            for item in fixture_data:
                fields = item['fields']
                fields['user'] = User.objects.get(id=fields.pop('user'))
                fields['movie'] = Movie.objects.get(id=fields.pop('movie'))
                fields['timestamp'] = fields.pop('timestamp')
                Comment.objects.create(**fields)

        elif model_name == 'movielens.image':
            for item in fixture_data:
                fields = item['fields']
                fields.pop('movie', None)
                image_file = fields.pop('img')
                movie_title = fields.pop('title')
                movie = Movie.objects.get(title=movie_title)
                Image.objects.create(title=movie_title, img=image_file, front_image=True, movie=movie)

        elif model_name == 'auth.user':
            for item in fixture_data:
                fields = item['fields']
                User.objects.create_user(**fields)

        else:
            call_command('loaddata', fixture_file)


if __name__ == '__main__':
    load_fixtures()
