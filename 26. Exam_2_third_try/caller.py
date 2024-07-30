import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from django.db.models import Q, Count, F
from main_app.models import Profile, Product, Order
from pprint import pprint


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by(
        'full_name'
    )

    if not profiles.exists():
        return ""

    result = []

    for p in profiles:
        result.append(
            f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        )

    return "\n".join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if profiles is None:
        return ""

    result = []

    for p in profiles:
        result.append(
            f"Profile: {p.full_name}, orders: {p.orders_count}"
        )

    return "\n".join(result)


def get_last_sold_products():
    last_orders = Order.objects.prefetch_related("products").last()

    if last_orders is None or not last_orders.products.exists():
        return ""

    result = []

    for product in last_orders.products.order_by("name"):
        result.append(
            product.name
        )

    return f"Last sold products: {', '.join(result)}"


def get_top_products():
    top_products = Product.objects.annotate(
        orders_count=Count('order_products')
    ).filter(
        orders_count__gt=0,
    ).order_by(
        '-orders_count',
        'name'
    )[:5]

    if not top_products.exists():
        return ""

    product_lines = "\n".join(f"{p.name}, sold {p.orders_count} times" for p in top_products)

    return f"Top products:\n" + product_lines


def apply_discounts():
    orders = Order.objects.annotate(
        product_count=Count('products')
    ).filter(
        product_count__gt=2,
        is_completed=False
    ).update(total_price=F("total_price") * 0.90)

    return f"Discount applied to {orders} orders."


def complete_order():
    order = Order.objects.filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ""

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return "Order has been completed!"
