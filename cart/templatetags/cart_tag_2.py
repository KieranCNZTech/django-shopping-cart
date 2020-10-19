from django import template
from typing import Union

Number = Union[int, float]

register = template.Library()


@register.filter
def subtotal(quantity: int, price: Number) -> float:
    """
    Returns a subtotal of the given inputs, quantity * price.
    :type quantity: Int
    :type price: Number (int or float).
    :return:
    """
    return int(quantity) * float(price)


@register.filter
def as_currency(amount: Number, rate: float = 1.0):
    """
    Formats the given amount as a currency.
    :type amount: Number (int or float).
    :param rate: Multiply 'amount' by 'rate'.
    :return: String in the format of "200.00".
    """
    total = float(amount) * float(rate)
    str_total = "{:,.2f}".format(total)

    return str_total


@register.filter
def product_total(quantity: int, price: Number) -> str:
    """
    Returns a subtotal of the given inputs, quantity * price.
    :type quantity: Int.
    :type price: Number (int or float).
    :return: String in the format of "$200.00".
    """
    qty = int(quantity)
    price = float(price)
    product_subtotal = subtotal(qty, price)
    return as_currency(product_subtotal)


@register.filter
def sum_cart(a) -> float:
    """
    Gets the subtotal of each item in the cart.
    :param a: List of products. Untyped as I'm unsure how 'dict_items' type truly works.
    :return: Float.
    """
    total = 0
    # a is of type 'dict_items'
    for i, this_tuple in enumerate(a):
        # key is product id, value is dictionary of product data
        values = this_tuple[1]
        qty = values['quantity']
        price = values['price']
        total += subtotal(qty, price)
    return total


@register.filter
def cart_total(a) -> str:
    """
    Calculates the total of the given list of products and returns a
        pretty representation.
    :param a: List of products. Untyped as I'm unsure how 'dict_items' type truly works.
    :return: Str in the format of "200.00".
    """
    total = sum_cart(a)
    return as_currency(total)


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
