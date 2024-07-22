import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order


# Create queries within functions

def get_profiles(search_string=None):
    if search_string is not None:
        query_name = Q(full_name__icontains=search_string)
        query_email = Q(email__icontains=search_string)
        query_phone_number = Q(phone_number__icontains=search_string)

        query = Profile.objects.annotate(num_orders=Count('order_profile')
                                         ).filter(query_name | query_email | query_phone_number
                                                  ).order_by("full_name")

        result = []

        for p in query:
            result.append(
                f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.num_orders}"
            )
        return "\n".join(result) if result else ""


def get_loyal_profiles():
    loyal_profile = Profile.objects.get_regular_customers()

    result = []

    for p in loyal_profile:
        result.append(
            f"Profile: {p.full_name}, orders: {p.orders_count}"
        )

    return "\n".join(result) if result else ""


def get_last_sold_products():
    try:
        last_order = Order.objects.prefetch_related('order_products').latest('creation_date')
        last_sold_products = last_order.products.all().order_by('name')

        result = []
        if last_sold_products:
            for p in last_sold_products:
                result.append(p.name)
            return f'"Last sold products: "{", ".join(result)}'
        return ""
    except Order.DoesNotExist:
        return ""

