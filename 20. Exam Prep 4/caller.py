import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from django.db.models import Q, Count, F
from main_app.models import Profile, Order, Product


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles.exists():
        return ""

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )


def get_loyal_profiles():
    loyal_prof = Profile.objects.get_regular_customers()

    if not loyal_prof.exists():
        return ""

    result = []

    for p in loyal_prof:
        result.append(
            f"Profile: {p.full_name}, orders: {p.order_count}"
        )

    return "\n".join(result)


def get_last_sold_products():
    last_order = Order.objects.prefetch_related("products").last()

    if last_order is None or not last_order.products.exists():
        return ""

    result = []

    for product in last_order.products.order_by("name"):
        result.append(
            product.name
        )

    return f'Last sold products: {", ".join(result)}'


def get_top_products():
    products = Product.objects.annotate(
        orders_count=Count("order")
    ).filter(
        orders_count__gt=0
    ).order_by("-orders_count", "name")

    if not products.exists():
        return ""

    result = ["Top products:"]

    for p in products:
        result.append(
            f"{p.name}, sold {p.orders_count} times"
        )

    return f"\n".join(result)


def apply_discounts():
    orders = Order.objects.annotate(
        product_count=Count("products")
    ).filter(
        product_count__gt=2,
        is_completed=False
    ).update(
        total_price=F("total_price") * 0.90
    )

    return f"Discount applied to {orders} orders."


def complete_order():
    order_complete = Order.objects.filter(
        is_completed=False
    ).order_by(
        "creation_date"
    ).first()

    if not order_complete:
        return ""

    for p in order_complete.products.all():
        p.in_stock -= 1

        if p.in_stock == 0:
            p.is_available = False
        p.save()

    order_complete.is_completed = True
    order_complete.save()

    return "Order has been completed!"