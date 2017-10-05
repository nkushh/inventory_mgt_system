from django.conf.urls import url

from . import views

app_name = 'authentication' 

urlpatterns = [
	url(r'^accounts/$', views.all_accounts, name='accounts'),
	url(r'^add-account/$', views.new_account, name='add_account'),
	url(r'^register-user/$', views.register_user, name='register_user'),
	url(r'^delete-account/(?P<account>\d+)/$', views.delete_account, name='delete-account'),
]