import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    profiles = Profile.objects.annotate(
        order_count=Count('orders')
    ).filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by(
        "full_name"
    )

    if profiles is None:
        return ""

    result = []

    for p in profiles:
        result.append(
            f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_count}"
        )

    return "\n".join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if profiles is None:
        return ""

    result = []

    for p in profiles:
        result.append(
            f"Profile: {p.full_name}, orders: {p.order_count}"
        )

    return "\n".join(result)


def get_last_sold_products():
    latest_order = Order.objects.prefetch_related("products").annotate(
        product_count=Count('products')
    ).filter(
        product_count__gt=0
    ).order_by(
        "-creation_date"
    ).first()

    if latest_order is None:
        return ""

    products = latest_order.products.values_list("name", flat=True).order_by("name")

    return f"Last sold products: {', '.join(products)}"


def get_top_products():
    top_products = Product.objects.annotate(num_orders=Count('order')) \
                       .filter(num_orders__gt=0) \
                       .order_by('-num_orders', 'name')[:5]

    if not top_products.exists():
        return ""

    products = ["Top products:"]

    for p in top_products:
        products.append(
            f"{p.name}, sold {p.num_orders} times"
        )

    return "\n".join(products)


def apply_discounts():
    orders = Order.objects.prefetch_related("products").annotate(
        product_count=Count("products")
    ).filter(
        product_count__gt=2,
        is_completed=False
    ).update(
        total_price=F("total_price") * 0.9
    )

    return f"Discount applied to {orders} orders."


def complete_order():
    oldest_order = Order.objects.filter(
        is_completed=False
    ).order_by(
        "creation_date"
    ).first()

    if oldest_order is None:
        return ""

    oldest_order.is_completed = True
    oldest_order.save()

    for product in oldest_order.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    return "Order has been completed!"
