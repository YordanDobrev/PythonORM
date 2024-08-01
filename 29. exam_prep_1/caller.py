import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from django.db.models import Q, Count, Avg
from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        directors = Director.objects.filter(query_name, query_nationality)
    elif search_name is not None:
        directors = Director.objects.filter(query_name)
    elif search_nationality is not None:
        directors = Director.objects.filter(query_nationality)
    else:
        return ""

    result = []

    for d in directors.order_by("full_name"):
        result.append(
            f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}"
        )

    return "\n".join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if director is None:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.movies_count}."


def get_top_actor():
    actor = Actor.objects.annotate(
        avg_rating=Avg('movie_starring_actor__rating')
    ).filter(
        avg_rating__gt=0
    ).order_by(
        "-avg_rating",
        "full_name"
    ).first()

    if actor is None:
        return ""

    movies = [movie.title for movie in actor.movie_starring_actor.all()]

    if len(movies) == 0:
        return ""

    return (f"Top Actor: {actor.full_name}, "
            f"starring in movies: {', '.join(movies)}, "
            f"movies average rating: {actor.avg_rating:.1f}")
