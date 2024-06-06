from django.db import models


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    time_registration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    photo_id = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'items'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        unique_together = ('user', 'item')
        managed = False
        db_table = 'cart'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_create = models.DateTimeField()
    status = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        unique_together = ('order', 'item')
        managed = False
        db_table = 'order_items'
