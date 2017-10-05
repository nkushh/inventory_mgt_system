from .models import Item_categorie, Item, Supplier, Item_sale, Item_supply
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
import datetime, calendar


# Create your views here.
@login_required(login_url='login')
def dashboard(request):
	today = datetime.datetime.now()
	mwaka = today.year

	accounts = User.objects.all().count()
	items = Item.objects.all()
	suppliers = Supplier.objects.all().count()
	sales = Item_sale.objects.filter(date_sold__year=mwaka, date_sold__month=today.month).aggregate(total_sales=Sum('amount'))
	expenses = Item_supply.objects.filter(date_supplied__year=mwaka, date_supplied__month=today.month).aggregate(total_expenses=Sum('amount'))
	sales_graph = Item_sale.objects.filter(date_sold__year=mwaka, date_sold__month=today.month).values('item').annotate(total_amount=Sum('amount'))
	current_month_sales = Item_sale.objects.filter(date_sold__year=mwaka, date_sold__month=today.month).aggregate(current_month=Sum('amount'))

	context = {
		'accounts' : accounts,
		'current_month_sales' : current_month_sales,
		'expenses' : expenses,
		'items' : items,
		'sales' : sales,
		'sales_graph' : sales_graph,
		'suppliers' : suppliers,
	}

	return render(request, "inventory/dashboard.html", context)

@login_required(login_url='login')
def item_categories(request):
	categories = Item_categorie.objects.all()

	context = {
		'categories' : categories,
	}

	return render(request, 'inventory/item-categories.html', context)

@login_required(login_url='login')
def register_category(request):
	if request.method=="POST":
		category_name = request.POST['category_name']
		if Item_categorie.objects.filter(category_name=category_name).exists():
			messages.error(request, "Error! That category name already exists. Try another one.")
			return redirect('inventory:item_categories')
		else:
			category = Item_categorie(category_name=category_name).save()
			messages.success(request, "Success! Item category details have been added.")
			return redirect('inventory:item_categories')
	else:
		return redirect('inventory:item_categories')

@login_required(login_url='login')
def category_detail(request, pk):
	category = get_object_or_404(Item_categorie, pk=pk)
	context = {
		'category' : category,
	}

	return render(request, 'inventory/category-items.html', context)


# Suppliers module
@login_required(login_url='login')
def new_supplier(request):
	return render(request, "inventory/new-supplier.html")

@login_required(login_url='login')
def register_supplier(request):
	if request.method=="POST":
		supplier_name = request.POST['supplier_name']
		contact = request.POST['contact']
		if Supplier.objects.filter(supplier_name=supplier_name).exists():
			messages.error(request, "Error! That supplier name already exists. Try another one.")
			return redirect('inventory:suppliers')
		else:
			supplier = Supplier(supplier_name=supplier_name, contact=contact).save()
			messages.success(request, "Success! Supplier details have been added.")
			return redirect('inventory:suppliers')
	else:
		return redirect('inventory:suppliers')

@login_required(login_url='login')
def suppliers(request):
	suppliers = Supplier.objects.all()
	context = {
		'suppliers' : suppliers,
	}

	return render(request, 'inventory/suppliers.html', context)


# Items module
@login_required(login_url='login')
def new_item(request):
	categories = Item_categorie.objects.all()

	context = {
		'categories' : categories,
	}

	return render(request, "inventory/new-item.html", context)

@login_required(login_url='login')
def register_item(request):
	if request.method=="POST":
		category = get_object_or_404(Item_categorie, pk=request.POST['category'])
		item_name = request.POST['item_name']
		brand = request.POST['brand']
		description = request.POST['description']
		quantity = request.POST['quantity']
		price = request.POST['price']
		if Item.objects.filter(category=category, item_name=item_name).exists():
			item = get_object_or_404(Item, item_name=item_name)
			item.quantity = item.quantity + quantity
			item.save()
			messages.warning(request, "Warning! That item name already exists. It's quantity has been updated.")
			return redirect('inventory:category_detail', pk=category.pk)
		else:
			item = Item(category=category, item_name=item_name, brand=brand, description=description, quantity=quantity, price=price).save()
			messages.success(request, "Success! Item details have been added.")
			return redirect('inventory:category_detail', pk=category.pk)
	else:
		return redirect('inventory:new_item')


@login_required(login_url='login')
def get_item(request, item):
	item = get_object_or_404(Item, pk=item)
	context = {
		'item' : item,
	}

	return render(request, 'inventory/record-sale.html', context)

@login_required(login_url='login')
def add_stock(request, item):
	item = get_object_or_404(Item, pk=item)
	context = {
		'item' : item,
	}

	return render(request, 'inventory/add-stock.html', context)

@login_required(login_url='login')
def update_stock(request):
	if request.method == "POST":
		item = get_object_or_404(Item, pk=request.POST['item'])
		item.quantity = item.quantity + float(request.POST['quantity'])
		item.save()
		messages.success(request, "Success! Item stock record updated successfully!")
		return redirect('inventory:sales')
	else:
		return redirect('inventory:sales')





# Sales module
@login_required(login_url='login')
def sales(request):
	sales = Item_sale.objects.all()
	items = Item.objects.all()

	context = {
		'sales' : sales,
		'items' : items,
	}

	return render(request, 'inventory/sales-records.html', context)

@login_required(login_url='login')
def record_sale(request):
	if request.method == "POST":
		item = get_object_or_404(Item, pk=request.POST['item'])
		quantity = float(request.POST['quantity'])
		amount = float(item.price) * quantity

		if quantity > item.quantity:
			messages.error(request, "Error! The quantity exceeds the available stock!")
			return redirect('inventory:sales')
		else:
			sale = Item_sale(item = item, quantity=quantity, amount=amount).save()
			item.quantity = item.quantity - quantity
			item.save()
			messages.success(request, "Success! Sale record details added!")
			return redirect('inventory:sales')
	else:
		return redirect('inventory:sales')


# Supply records module
@login_required(login_url='login')
def new_supply_record(request):
	suppliers = Supplier.objects.all()

	context = {
		'suppliers' : suppliers,
	}

	return render(request, "inventory/add-supply.html", context)


@login_required(login_url='login')
def record_supply(request):
	if request.method == "POST":
		supplier = get_object_or_404(Supplier, pk=request.POST['supplier'])
		items_supplied = request.POST['items_supplied']
		item_brand = request.POST['item_brand']
		quantity = float(request.POST['quantity'])
		amount = float(request.POST['amount'])

		
		supply = Item_supply(supplier=supplier, items_supplied=items_supplied, item_brand=item_brand, quantity=quantity, amount=amount).save()
		messages.success(request, "Success! Supply record details added!")
		return redirect('inventory:supply_records')
	else:
		return redirect('inventory:supply_records')


@login_required(login_url='login')
def supply_records(request):
	records = Item_supply.objects.all().order_by('-date_supplied')
	suppliers = Supplier.objects.all()

	context = {
		'records' : records,
		'suppliers' : suppliers,
	}

	return render(request, 'inventory/supply-records.html', context)






			

