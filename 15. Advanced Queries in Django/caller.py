import os
import django
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Product, Order


def product_quantity_ordered():
    result = []
    orders = Product.objects.annotate(
        total=Sum('orderproduct__quantity')
    ).values("name", "total").order_by("-total")

    for order in orders:
        result.append(
            f"Quantity ordered of {order['name']}: {order['total']}"
        )

    return "\n".join(result)


def ordered_products_per_customer():
    order = Order.objects.prefetch_related("orderproduct_set__product__category").order_by("id")

    result = []

    for o in order:
        result.append(f"Order ID: {o.id}, Customer: {o.customer.username}")

        for p in o.orderproduct_set.all():
            result.append(
                f"- Product: {p.product.name}, Category: {p.product.category.name}"
            )

    return "\n".join(result)


def filter_products():
    query = Q(is_available=True) & Q(price__gt=3.00)
    products = Product.objects.filter(query).order_by("-price", "name")

    result = []
    for product in products:
        result.append(
            f"{product.name}: {product.price}lv."
        )

    return "\n".join(result)


def give_discount():
    query = Q(is_available=True) & Q(price__gt=3.00)
    reduction = F("price") * 0.7
    products = Product.objects.filter(
        query
    ).update(price=reduction)

    available_products = Product.objects.filter(
        is_available=True
    ).order_by("-price", "name")

    result = []

    for p in available_products:
        result.append(f"{p.name}: {p.price}lv.")

    return "\n".join(result)
