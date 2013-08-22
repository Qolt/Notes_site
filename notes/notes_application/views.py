# Create your views here.
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

def show_start_page(request):
    if request.user.is_authenticated():
        return render_to_response('index.html', {'user': request.user.first_name + " " + request.user.last_name })
    else:
        return render_to_response('index.html', {'user': "Anonymous"})

def show_login_page(request):
    return render_to_response('login.html', {})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
