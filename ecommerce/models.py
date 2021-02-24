from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from user.models import User


class Tag(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.title


class Info(models.Model):
    item = models.ForeignKey(to='Item', on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return f"""<{self.item}, {self.item.id}> {self.title}"""


class ItemImage(models.Model):
    image = models.ImageField(upload_to=f"""ecommerce/item-images""")
    item = models.ForeignKey(to='Item', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.item}, <{self.id}>"


class Item(models.Model):
    name = models.CharField(max_length=200)
    tag = models.ManyToManyField(to='Tag')
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

    quantity = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0'))])

    # @TODO: condition - (new, used-good, used-normal, used-damaged)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    item = models.ForeignKey(to='Item', on_delete=models.CASCADE)
    cart = models.ForeignKey(to='Cart', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

    price = models.DecimalField(default=0, max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0'))])

    ordered = models.DateTimeField(auto_now_add=True)

    StatusChoices = [
        ('Pending', 'pending'),
        ('Shipped', 'shipped'),
        ('Delivered', 'delivered')
    ]

    status = models.CharField(choices=StatusChoices, max_length=30, default='Pending')

    # @TODO: deliver_from - address
    # @TODO: deliver_to - address

    # @TODO: ordered - time when user placed order

    def __str__(self) -> str:
        return f'<{self.user}>, {self.id}'


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    # @TODO: total - sum of order_set price

    def get_total_price(self) -> Decimal:
        return round(self.order_set.aggregate(Sum('price'))['price__sum'], 2) if self.order_set.all() else 0

    def __str__(self) -> str:
        return f'<{self.user}>, {self.id}'
