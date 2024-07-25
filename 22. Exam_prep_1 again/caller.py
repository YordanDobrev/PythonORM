import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
from django.db.models import Q, Count, Avg, Max, F


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = query_name
    else:
        query = query_nationality
    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = []
    for d in directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality},"
                      f" experience: {d.years_of_experience}")

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."


def get_top_actor():
    top_actor = Actor.objects.prefetch_related("starring_movies").annotate(
        movie_count=Count("starring_movies"),
        avg_rating=Avg("starring_movies__rating"),
    ).order_by("-movie_count", "full_name").first()

    if not top_actor or not top_actor.movie_count:
        return ''

    movies = ', '.join(m.title for m in top_actor.starring_movies.all() if m)

    return (f"Top Actor: {top_actor.full_name}, starring in movies: {movies},"
            f" movies average rating: {top_actor.avg_rating:.1f}")


def get_actors_by_movies_count():
    actors = Actor.objects.prefetch_related("movies").annotate(
        movie_count=Count("movies"),
    ).order_by("-movie_count", "full_name")[:3]

    if not actors or not actors[0].movie_count:
        return ""

    result = []

    for a in actors:
        result.append(
            f"{a.full_name}, participated in {a.movie_count} movies"
        )

    return "\n".join(result)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.select_related("starring_actor").prefetch_related("actors").filter(
        is_awarded=True
    ).order_by(
        "-rating", "title"
    ).first()

    if top_movie is None:
        return ""

    all_actors = []

    for actor in top_movie.actors.order_by("full_name"):
        all_actors.append(
            actor.full_name
        )

    staring_actor = top_movie.starring_actor.full_name

    if not top_movie.starring_actor.full_name:
        staring_actor = 'N/A'

    return (f"Top rated awarded movie: {top_movie.title}, "
            f"rating: {top_movie.rating:1f}. "
            f"Starring actor: {staring_actor}. "
            f"Cast: {', '.join(all_actors)}.")


def increase_rating():
    classic_movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10
    ).update(rating=F("rating") + 0.1)

    if not classic_movies:
        return "No ratings increased."

    return f"Rating increased for {classic_movies} movies."
