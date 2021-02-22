from django.db import models


class Tag(models.Model):
    # @TODO: title
    pass


class Info(models.Model):
    # @TODO: title
    # @TODO: description
    pass


class ItemImage(models.Model):
    # @TODO: image
    # @TODO: Item - 1 to many
    pass


class Item(models.Model):
    # @TODO: tags - many to many
    # @TODO: seller (User) - 1 to many

    # @TODO: available - boolean
    pass


class IndividualItem(models.Model):
    # @TODO: Info - many to many
    # @TODO: Item - 1 to many
    # @TODO: condition - (new, used-good, used-normal, used-damaged)
    # @TODO: price
    pass


class Order(models.Model):
    # @TODO: IndividualItem - 1 to 1
    # @TODO: Cart - 1 to many
    # @TODO: buyer (User) - 1 to many

    # @TODO: price - Q+

    # @TODO: deliver_from - address
    # @TODO: deliver_to - address

    # @TODO: ordered - time when user placed order
    pass


class Cart(models.Model):
    # @TODO: User - 1 to 1
    # @TODO: total - sum of order_set price
    pass
