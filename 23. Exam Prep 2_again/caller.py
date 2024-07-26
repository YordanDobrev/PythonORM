import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, F
from main_app.models import Profile, Order, Product


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles.exist():
        return ""

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ""

    return "\n".join(
        f"Profile: {p.full_name}, orders: {p.orders.count()}"  # p.orders_count
        for p in profiles
    )


def get_last_sold_products():
    latest_orders = Order.objects.prefetch_related("products").last()

    if latest_orders is None or not latest_orders.products.exists():
        return ""

    products = latest_orders.products.order_by("name").values_list("name", flat=True)

    return f'Last sold products: {", ".join(products)}'


def get_top_products():
    top_products = Product.objects.annotate(
        orders_count=Count("orders")
    ).filter(
        orders_count__gt=0
    ).order_by(
        "-orders_count",
        "name"
    )[:5]

    if not top_products.exists():
        return ""

    result = ["Top products:"]

    for product in top_products:
        result.append(
            f"{product.name}, sold {product.orders_count} times"
        )

    return "\n".join(result)


def apply_discounts():
    discounted_products = Order.objects.annotate(
        product_count=Count("products")
    ).filter(
        is_completed=False,
        product_count__gt=2
    ).update(
        total_price=F("total_price") * 0.9
    )

    return f"Discount applied to {discounted_products} orders."


def complete_order():
    latest = Order.objects.filter(
        is_completed=False,
    ).order_by(
        "creation_date"
    ).last()

    if not latest:
        return ""

    for product in latest.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    latest.is_completed = True
    latest.save()

    return "Order has been completed!"