from django.contrib import admin
from .models import Item_categorie, Item, Supplier, Item_sale, Item_supply

# Register your models here.
admin.site.register(Item_categorie)
admin.site.register(Item)
admin.site.register(Supplier)
admin.site.register(Item_sale)
admin.site.register(Item_supply)
