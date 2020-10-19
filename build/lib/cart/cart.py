from django.conf import settings


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        # Makes an empty cart if one does not exist then save it.
        self.cart = self.session.get(settings.CART_SESSION_ID, {})
        if self.cart == {}:
            self.save()

    def add(self, product, quantity: int = 1):
        """
        Add a product to the cart.
          If the product is already in the cart, will call edit_quantity.
        :param product: Product to add to the cart. Stores the ID, name, and price.
        :param quantity: How much of the product to add to the cart.
        """
        p_id = product.id
        p_id_str = str(p_id)
        if p_id_str not in self.cart.keys():
            self.cart[p_id] = {
                'userid': self.request.user.id,
                'product_id': p_id,
                'name': product.name,
                'quantity': int(quantity),
                'price': str(product.price)
            }
        else:
            self.cart[p_id_str]['quantity'] += quantity

        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        p_id = str(product.id)
        if p_id in self.cart:
            del self.cart[p_id]
            self.save()

    def edit_quantity(self, product, new_qty: int):
        """
        Edits the amount of a product in the cart.
          If the product is not in the cart, will call add.
        :param product: Product to edit the quantity of.
        :param new_qty: New quantity to give to the product. Will remove the product is this reaches 0.
        """
        p_id = product.id
        p_id_str = str(p_id)
        if p_id_str in self.cart.keys():
            if new_qty == 0:
                self.remove(product)
            else:
                self.cart[p_id_str]['quantity'] = new_qty
            self.save()

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
