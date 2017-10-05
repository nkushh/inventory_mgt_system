from django.conf.urls import url

from . import views

app_name = 'inventory'

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
	# Categories
	url(r'^item-categories/$', views.item_categories, name='item_categories'),
	url(r'^register-category/$', views.register_category, name='register_category'),
	url(r'^category/(?P<pk>\d+)/detail/$', views.category_detail, name='category_detail'),
	# Suppliers
	url(r'^new-supplier/$', views.new_supplier, name='new_supplier'),
	url(r'^register-supplier/$', views.register_supplier, name='register_supplier'),
	url(r'^suppliers/$', views.suppliers, name='suppliers'),
	# Items
	url(r'^new-item/$', views.new_item, name='new_item'),
	url(r'^register-item/$', views.register_item, name='register_item'),
	url(r'^add-stock/(?P<item>\d+)/$', views.add_stock, name='add_stock'),
	url(r'^update-stock/$', views.update_stock, name='update_stock'),
	# Sale
	url(r'^sales/$', views.sales, name='sales'),
	url(r'^get-item/(?P<item>\d+)/$', views.get_item, name='get_item'),
	url(r'^record-sale/$', views.record_sale, name='record_sale'),
	# Supply records
	url(r'^supply-records/$', views.supply_records, name='supply_records'),
	url(r'^add-supply/$', views.new_supply_record, name='add_supply_record'),
	url(r'^register-supply/$', views.record_supply, name='record_supply'),
]