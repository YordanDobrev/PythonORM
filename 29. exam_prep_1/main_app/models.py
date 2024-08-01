from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager
from main_app.mixins import IsAwarded, LastUpdated


# Create your models here.
class Person(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )

    birth_date = models.DateField(
        default='1900-01-01'
    )

    nationality = models.CharField(
        max_length=50,
        default="Unknown"
    )


class Director(Person):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    objects = DirectorManager()


class Actor(Person, IsAwarded, LastUpdated):
    pass


class Movie(IsAwarded, LastUpdated):
    class MovieGenre(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=MovieGenre.choices,
        default=MovieGenre.OTHER,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ]
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='movie',
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='movie_starring_actor',
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='movie_actors',
    )
