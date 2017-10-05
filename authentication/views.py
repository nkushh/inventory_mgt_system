from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

@login_required(login_url='login')
def new_account(request):
	return render(request, 'authentication/create-account.html')

@login_required(login_url='login')
def register_user(request):
	if request.method=='POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']

		if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
			User.objects.create_user(username, email, password)
			messages.success(request, "Success! Account detail successfully recorded.")
			return redirect('authentication:accounts')
		else:
			messages.warning(request, "Error! Username with that email already exists")
			return redirect('authentication:register_user')

	else:
		return render(request, 'authentication/register-user.html')

@login_required(login_url='login')
def all_accounts(request):
	users = User.objects.all()
	context = {
		'users' : users,
	}
	return render(request, 'authentication/accounts.html', context)


@login_required(login_url='login')
def delete_account(request, account):
	farm = get_object_or_404(User, pk=account)
	farm.delete()
	messages.success(request, 'Account successfully deleted')
	return redirect('authentication:accounts')
