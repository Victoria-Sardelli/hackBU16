from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login, models


# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('chalk_schedule'))
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('chalk_schedule'))
        else:
            return render(request, 'clogin.html', {
                'message': 'Username or password are incorrect',
            })


def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('chalk_home'))


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('chalk_schedule'))
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_conf = request.POST.get('password_conf')
        if password is not password_conf:
            return render(request, 'index.html', {
                'error': 'Passwords do not match!',
            })
        user = models.User.objects.create_user(username, email=email, password=password)
        user.save()
        authenticate(user.username, user.password)
        return HttpResponseRedirect(reverse("chalk_schedule"))
    return render(request, 'index.html')

def new_entries(request):
    pass


def schedule(request):
    return HttpResponse("Welcome!")
