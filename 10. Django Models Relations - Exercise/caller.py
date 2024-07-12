import os
from datetime import timedelta, date, datetime

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Book, Author, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car
from django.db.models import QuerySet


# Create queries within functions

def show_all_authors_with_their_books():
    authors_with_books = []
    authors = Author.objects.all().order_by("id")

    for a in authors:

        books = Book.objects.filter(author=a)

        if not books:
            continue

        titles = ", ".join(b.title for b in books)

        authors_with_books.append(
            f"{a.name} has written - {titles}!"
        )

    return "\n".join(authors_with_books)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)  # SELECT * FROM artist WHERE name = "Eminem"
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)  # remove, clear

    # Artist.objects.get(name=artist_name).songs.add(Song.objects.get(title=song_title))


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    return Artist.objects.get(name=artist_name).songs.all().order_by("-id")


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)  # SELECT * FROM artist WHERE name = "Eminem"
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)
    # song.artists.remove(artist) the same


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()

    total_rating = sum(r.rating for r in reviews)
    average_rating = total_rating / len(reviews)

    return average_rating


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by("-name")


def delete_products_without_reviews():
    get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates():
    result = []
    licence = DrivingLicense.objects.all().order_by("-license_number")

    for l in licence:
        expiration_date = l.issue_date + timedelta(days=365)
        result.append(f"License with number: {l.license_number} expires on {expiration_date}!")

    return "\n".join(result)


def get_drivers_with_expired_licenses(due_date: date):
    return Driver.objects.filter(license__issue_date__gt=(due_date - timedelta(days=365)))


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner
    car.save()

    registration.registration_date = date.today()
    registration.car = car

    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."