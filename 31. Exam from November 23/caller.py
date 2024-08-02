import os
from pprint import pprint

import django
from django.db.models import Q, Count, Avg, Max

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review


# Create queries within functions

def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(
            Q(full_name__icontains=search_name) & Q(email__icontains=search_email)).order_by('-full_name')
    elif search_name is not None:
        authors = Author.objects.filter(Q(full_name__icontains=search_name)).order_by('-full_name')
    else:
        authors = Author.objects.filter(Q(email__icontains=search_email)).order_by('-full_name')

    result = []

    for a in authors:
        banned = "Banned" if a.is_banned else "Not Banned"

        result.append(
            f"Author: {a.full_name}, email: {a.email}, status: {banned}"
        )

    return "\n".join(result) if result else ""


def get_top_publisher():
    publisher = Author.objects.get_authors_by_article_count().first()

    if publisher is None or publisher.article_count == 0:
        return ""
    return f"Top Author: {publisher.full_name} with {publisher.article_count} published articles."


def get_top_reviewer():
    author = Author.objects.annotate(
        review_count=Count('reviews')
    ).order_by(
        '-review_count',
        'email'
    ).first()

    if author is None or author.review_count == 0:
        return ""

    return f"Top Reviewer: {author.full_name} with {author.review_count} published reviews."


def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()

    if latest_article is None:
        return ""

    avg_rating = sum([r.rating for r in latest_article.reviews.all()]) / latest_article.reviews.count()

    authors = ', '.join([a.full_name for a in latest_article.authors.order_by('full_name')])

    return (f"The latest article is: {latest_article.title}. "
            f"Authors: {authors}. "
            f"Reviewed: {latest_article.reviews.count()} times. "
            f"Average Rating: {avg_rating:.2f}.")

def get_top_rated_article():
    article = Article.objects.prefetch_related('reviews').annotate(
        avg_review=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(
        avg_review__gt=0,
    ).order_by(
        '-avg_review',
        'title'
    ).first()

    if article is None or article.review_count == 0:
        return ""

    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {article.avg_review:.2f}, "
            f"reviewed {article.review_count} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    author = Author.objects.filter(email__exact=email).first()
    if author is None:
        return "No authors banned."

    reviews_count = author.reviews.count()
    author.is_banned = True
    author.save()
    author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {reviews_count} reviews deleted."
