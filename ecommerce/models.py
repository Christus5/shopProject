from django.db import models
from django.db.models import Sum

from user.models import User


class Tag(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.title


class Info(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class ItemImage(models.Model):
    image = models.ImageField(upload_to=f"""ecommerce/item-images""")
    item = models.ForeignKey(to='Item', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.item}, <{self.id}>"


class Item(models.Model):
    name = models.CharField(max_length=200)
    tag = models.ManyToManyField(to='Tag')
    info = models.ForeignKey(to='Info', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

    quantity = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)
    price = models.PositiveIntegerField()

    # @TODO: condition - (new, used-good, used-normal, used-damaged)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    item = models.ForeignKey(to='Item', on_delete=models.CASCADE)
    cart = models.ForeignKey(to='Cart', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

    price = models.PositiveIntegerField()

    ordered = models.DateTimeField(auto_now_add=True)

    # @TODO: deliver_from - address
    # @TODO: deliver_to - address

    # @TODO: ordered - time when user placed order

    def __str__(self) -> str:
        return f'<{self.user}>, {self.id}'


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    # @TODO: total - sum of order_set price

    def get_total_price(self) -> int:
        return self.order_set.aggregate(Sum('price'))['price__sum']

    def __str__(self) -> str:
        return f'<{self.user}>, {self.id}'
