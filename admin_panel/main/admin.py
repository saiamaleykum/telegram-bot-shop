from django.contrib import admin
from .models import User, Category, Item, Cart, Order, OrderItem

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
