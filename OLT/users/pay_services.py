import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name, description):
    """
    Создаем продукт в Stripe
    """
    product = stripe.Product.create(
        name=name,
        description=description
    )
    return product.id


def create_price(product_id, price_sum, currency):
    """
    Создаем цену в Stripe
    """

    if price_sum is not None:
        price_val = int(price_sum) * 100  # Цена должна быть только в копейках
        price = stripe.Price.create(
            product=product_id,
            unit_amount=price_val,
            currency=currency
        )
        return price.id
    else:
        return None


def create_session(price_id, success_url, cancel_url):
    """
    Создаем сессию для платежа в Stripe
    """
    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1
            }
        ],
        mode="payment"
    )
    return session.url
