# Create your views here.
from forms import *
from django.template import RequestContext
from django.contrib import auth
from models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
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

def method_splitter(request, GET=None, POST=None):
    if request.method == 'GET' and GET is not None:
        return GET(request, show_first = True)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    raise Http404

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
def notes_list(request, note_id=0, show_first=False):
    assert request.method == 'GET'
    user_notes = Notes.objects.filter(owner = request.user)
    try:
        note_text = Notes.objects.get(owner = request.user, id = note_id)
        text = note_text.text
    except:
        text = ""  #user_notes[0].text
    return render_to_response('notes_list.html', {'notes': user_notes, 
                                                  'note_text': text, 
                                                  'note_id': note_id, 
                                                  'show_first': show_first})

@login_required
def save_note(request):
    assert request.method == 'POST' 
    form = NoteForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        Notes(title = clean_data['title'], text = clean_data['text'], owner = request.user).save()
        return HttpResponseRedirect('/notes_list/')


@login_required
def note_content(request, note_id=0):
    try:
        note_text = Notes.objects.get(owner = request.user, id = note_id)
        text = note_text.text
    except:
        text = ""
    return render_to_response('note_template.html', {'note_text': text, 'note_id': note_id})

@login_required
def delete_note(request, note_id=0):
    try:
        note = Notes.objects.get(owner = request.user, id = note_id)
        note.delete()
    except:
        pass
    return HttpResponseRedirect('/notes_list/')
