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
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    raise Http404

@login_required
def edit_note(request, note_id=0):
    try:
        note = Notes.objects.get(owner = request.user, id = note_id)
        title = note.title
        text = note.text
    except:
        title = ""
        text = ""
    form = NoteForm(
        initial={'title': title, 'text': text}
    )
    return render_to_response('edit_note.html', {'form': form, 'note_id': note_id}, context_instance=RequestContext(request))

@login_required
def create_note(request):
    form = NoteForm()
    return render_to_response('create_note.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def notes_list(request, note_id=0):
    assert request.method == 'GET'
    user_notes = Notes.objects.filter(owner = request.user)
    try:
        note_text = Notes.objects.get(owner = request.user, id = note_id)
        text = note_text.text
    except:
        text = ""  #user_notes[0].text
    if note_id == 0:
        note_id = user_notes[0].id
    return render_to_response('notes_list.html', {'notes': user_notes, 
                                                  'note_text': text, 
                                                  'note_id': note_id})

@login_required
def save_note(request, note_id=None):
    assert request.method == 'POST' 
    form = NoteForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        if note_id:
            note = Notes.objects.get(owner = request.user, id = note_id)
            note.text = clean_data['text']
            note.title = clean_data['title']
            note.save()
        else:
            Notes(title = clean_data['title'], text = clean_data['text'], owner = request.user).save()
        return HttpResponseRedirect('/note_content/' + note_id)


@login_required
def note_content(request, note_id=0):
    try:
        note = Notes.objects.get(owner = request.user, id = note_id)
        text = note.text
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
