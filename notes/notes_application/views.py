# Create your views here.
from forms import *
from django.template import RequestContext
from django.contrib import auth
from models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from models import Notes

def show_start_page(request):
    if request.user.is_authenticated():
        return render_to_response('index.html', {'user': request.user.first_name  
            + " " + request.user.last_name })
    else:
        return render_to_response('index.html', {'user': "Anonymous"})

def show_login_page(request):
    return render_to_response('login.html', {})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            Notes(title = clean_data['title'], text = clean_data['text'], owner = request.user).save()
            return HttpResponseRedirect('/')
    else:
        form = NoteForm()
    return render_to_response('create_note.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def notes_list(request, note_id=0):
    user_notes = Notes.objects.filter(owner = request.user)
    try:
        note_text = Notes.objects.get(owner = request.user, id = note_id)
        text = note_text.text
    except:
        text = ""
    return render_to_response('notes_list.html', {'notes': user_notes, 'note_text': text})
