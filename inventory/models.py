from django.db import models
from django.utils import timezone

# Create your models here.

class Item_categorie(models.Model):
	category_name = models.CharField(max_length=200)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.category_name

class Item(models.Model):
	category = models.ForeignKey(Item_categorie)
	item_name = models.CharField(max_length=200)
	brand = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	quantity = models.FloatField(default=0)
	price = models.FloatField()
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.item_name

class Supplier(models.Model):
	supplier_name = models.CharField(max_length=200)
	contact = models.CharField(max_length=200)
	added_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.supplier_name

class Item_sale(models.Model):
	item = models.ForeignKey(Item)
	quantity = models.FloatField()
	amount = models.FloatField()
	date_sold = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{} - {}".format(self.item, self.quantity)

class Item_supply(models.Model):
	supplier = models.ForeignKey(Supplier)
	items_supplied = models.CharField(max_length=200)
	item_brand = models.CharField(max_length=200, blank=True)
	quantity = models.FloatField()
	amount = models.FloatField()
	date_supplied = models.DateField(default=timezone.now)
	pay_status = models.IntegerField(default=0)

	def __str__(self):
		return "supplier: {}, Items: {}, Quantity: {}".format(self.supplier, self.items_supplied, self.quantity)

