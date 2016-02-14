from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login as lin
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User as U

from . import models


# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('chalk_schedule'))
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            lin(request, user)
            return HttpResponseRedirect(reverse('chalk_schedule'))
        else:
            return render(request, 'clogin.html', {
                'success': False,
                'message': 'Username or password are incorrect',
            })
    return render(request, 'clogin.html', {})


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('chalk_schedule'))
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_conf = request.POST.get('password_conf')
        if password != password_conf:
            return render(request, 'index.html', {
                'error': 'Passwords do not match!',
            })
        if len(U.objects.filter(username=username))>0:
            return render(request, 'index.html', {
                'error': 'Username already taken!',
            })
        if len(U.objects.filter(email=email))>0:
            return render(request, 'index.html', {
                'error': 'Email already taken!',
            })
        user = U.objects.create_user(username=username, email=email, password=password)
        user.first_name = "User"
        user.last_name = "Name"
        user.is_active = True
        user.save()
        var = authenticate(username=username, password=password)
        lin(request, var)
        return HttpResponseRedirect(reverse("chalk_schedule"))
    return render(request, 'index.html')


def new_entries(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("chalk_home"))
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        approx_time = request.POST.get('duration')
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
    return render(request, "entries.html")


def schedule(request):
    if request.user is None or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('chalk_home'))
    act_list = models.Activity.objects.filter(owner=request.user).exclude(due_date__lt=date.today())
    if len(act_list) < 1:
        return render(request, "schedule.html")
    slist = []
    for i in range(0, 6):
        for item in act_list:
            if item.priority == i:
                slist.append(item)
    stimes = []
    stimes.append(datetime.now())
    for item in slist:
        stimes.append(stimes[len(stimes)-1]+timedelta(hours=item.approx_time))
    str1 = ""
    for i in range(0, len(slist)):
        str1 += "{ title: '" + slist[i].title + "', start: new Date('" + str(stimes[i]) + "'), end: new Date('" + str(stimes[i+1]) + "')}"
        if i < len(slist)-1:
            str1 += ", "
    return render(request, 'schedule.html', {
        'jq': str1,
    })


def contact(request):
    return render(request, "contact.html", {})


def about(request):
    return render(request, "about_us.html", {})


def free(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("chalk_home"))
    if request.method == "POST":
        start_time = request.POST.get("start_time")
        start_time = datetime.strptime(start_time, "%b/%d/%Y %I:%M")
        end_time = request.POST.get("end_time")
        end_time = datetime.strptime(end_time, "%b/%d/%Y %I:%M")
        free = Frees(start_time=start_time, end_time=end_time)
        free.save()
    return render(request, 'free.html')