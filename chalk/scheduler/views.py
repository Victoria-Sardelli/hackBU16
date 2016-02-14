from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login, decorators
from datetime import date

from . import models


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


@decorators.login_required
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
        user = models.User(username=username, email=email, password=password)
        user.save()
        authenticate(user.username, user.password)
        return HttpResponseRedirect(reverse("chalk_schedule"))
    return render(request, 'index.html')


def new_entries(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        approx_time = request.POST.get('approx_time')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        if not priority.isdigit():
            priority = 0
        activity = models.Activity(title=title,
                                   description=description,
                                   approx_time=approx_time,
                                   due_date=due_date,
                                   priority=priority)
        activity.owner = request.user
        activity.save()
        if activity is not None:
            return render(request, 'entries.html', {
                'success': True,
                'message': 'Successfully added task.',
            })
        else:
            return render(request, 'entries.html', {
                'success': False,
                'message': 'Could not add task.',
            })


def schedule(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('chalk_home'))
    act_list = models.Activity.objects.get(owner=request.user, due_date__gte=date.today())
    return render(request, 'schedule.html', {
        'activities': act_list,
    })
