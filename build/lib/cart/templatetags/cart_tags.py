from django import template
from typing import Union

Number = Union[int, float]

register = template.Library()


@register.filter
def product_subtotal(product) -> float:
    """
    Returns a subtotal of the product, quantity * price.
    :type product: Dictionary.
    :return:
    """
    try:
        return int(product["quantity"]) * float(product["price"])
    except KeyError as key_err:
        pass


@register.filter
def as_currency(amount: Number, rate: float = 1.0):
    """
    Formats the given amount as a currency.
    :type amount: Number (int or float).
    :param rate: Multiply 'amount' by 'rate'.
    :return: String in the format of "2,000.00".
    """
    total = float(amount) * float(rate)
    str_total = "{:,.2f}".format(total)

    return str_total


@register.simple_tag
def product_total(product, rate: float = 1.0) -> str:
    """
    Returns a pretty subtotal of the given product.
    :type product: Dictionary.
    :param rate: Float representing the exchange rate.
    :return: String in the format of "2,000.00".
    """
    p_subtotal = product_subtotal(product)
    return as_currency(p_subtotal, rate=rate)


@register.filter
def cart_subtotal(a) -> float:
    """
    Gets the subtotal of each item in the cart.
    :param a: List of products. Untyped as I'm unsure how 'dict_items' type truly works.
    :return: Float.
    """
    total = 0
    # a is of type 'dict_items'
    for i, this_tuple in enumerate(a):
        # key is product id, value is dictionary of product data
        product = this_tuple[1]
        total += product_subtotal(product)
    return total


@register.simple_tag
def cart_total(a, rate: float = 1.0) -> str:
    """
    Calculates the total of the given list of products and returns a
        pretty representation.
    :param a: List of products. Untyped as I'm unsure how 'dict_items' type truly works.
    :param rate: Float representing the exchange rate.
    :return: Str in the format of "200.00".
    """
    total = cart_subtotal(a)
    return as_currency(total, rate=rate)


@register.filter
def cart_count(a) -> int:
    """
    Count the number of items in the cart.
    :param a: List of products. Untyped as I'm unsure how 'dict_items' type truly works.
    :return: Int of the number of items in the cart.
    """
    count = 0
    # a is of type 'dict_items'
    for i, this_tuple in enumerate(a):
        # key is product id, value is dictionary of product data
        values = this_tuple[1]
        count += values['quantity']

    return count
