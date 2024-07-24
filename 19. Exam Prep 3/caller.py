import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app import models
from main_app.models import Author, Review, Article
from populate_db import populate_model_with_data


# Import your models here

# Create queries within functions
def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(full_name__icontains=search_name, email__icontains=search_email).order_by(
            '-full_name')

    elif search_name is not None:
        authors = Author.objects.filter(full_name__icontains=search_name).order_by('-full_name')

    else:
        authors = Author.objects.filter(email__icontains=search_email).order_by('-full_name')

    result = []
    [result.append(f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}") for
     a in authors if authors]

    return '\n'.join(result) if result else ''


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().first()

    if top_author is None or top_author.article_count == 0:
        return ''
    return f"Top Author: {top_author.full_name} with {top_author.article_count} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews', 'email').first()

    if top_reviewer is None or top_reviewer.num_reviews == 0:
        return ""
    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."


def get_latest_article():
    latest_article = Article.objects.prefetch_related('authors', 'reviews').order_by('-published_on').first()

    if latest_article is None:
        return ""

    authors_names = ', '.join(author.full_name for author in latest_article.authors.all().order_by('full_name'))
    num_reviews = latest_article.reviews.count()
    avg_rating = sum([r.rating for r in latest_article.reviews.all()]) / num_reviews if num_reviews else 0.0

    return f"The latest article is: {latest_article.title}. Authors: {authors_names}. Reviewed: {num_reviews} times." \
           f" Average Rating: {avg_rating:.2f}."

