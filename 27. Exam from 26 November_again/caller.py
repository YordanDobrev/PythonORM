import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article
from django.db.models import Q, Count, Avg


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query = query_name & query_email
    elif search_name is not None:
        query = query_name
    elif search_email is not None:
        query = query_email

    authors = Author.objects.filter(query)

    if authors is None:
        return ""

    result = []

    for a in authors.order_by("-full_name"):
        banned = "Banned" if a.is_banned else "Not Banned"
        result.append(
            f"Author: {a.full_name}, email: {a.email}, status: {banned}"
        )

    return "\n".join(result)


def get_top_publisher():
    authors = Author.objects.get_authors_by_article_count().first()

    if authors is None:
        return ""

    return f"Top Author: {authors.full_name} with {authors.article_count} published articles."


def get_top_reviewer():
    review = Author.objects.annotate(
        author_count=Count("reviews")
    ).filter(
        author_count__gt=0
    ).order_by(
        "-author_count",
        "email"
    ).first()

    if review is None or review.author_count == 0:
        return ""

    return f"Top Reviewer: {review.full_name} with {review.author_count} published reviews."


def get_latest_article():
    article = Article.objects.prefetch_related('authors', 'reviews').order_by('-published_on').first()

    if article is None:
        return ""

    result = []

    for a in article.authors.order_by("full_name"):
        result.append(a.full_name)

    num_reviews = article.reviews.count()
    avg_rating = sum([r.rating for r in article.reviews.all()]) / num_reviews if num_reviews else 0

    return (f"The latest article is: {article.title}. "
            f"Authors: {', '.join(result)}. "
            f"Reviewed: {num_reviews} times. "
            f"Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    article = Article.objects.annotate(
        review_count=Count("reviews"),
        avg_rating=Avg("reviews__rating"),
    ).order_by(
        "-reviews__rating",
        "title"
    ).first()

    if article is None or article.review_count == 0:
        return ""

    review_count = article.reviews.count() if article.review_count else 0

    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {article.avg_rating:.2f}, "
            f"reviewed {review_count} times.")


def ban_author(email=None):
    author = Author.objects.prefetch_related('reviews').filter(email__exact=email).first()

    if author is None or email is None:
        return "No authors banned."

    num_reviews_deleted = author.reviews.count()

    author.is_banned = True
    author.save()
    author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {num_reviews_deleted} reviews deleted."

print(get_latest_article())