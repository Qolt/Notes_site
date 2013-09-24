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
        username = request.user.first_name + " " + request.user.last_name
        if username == " ":
            username = request.user.username
        return render_to_response('index.html', {'user': username})
    else:
        return render_to_response('index.html', {'user': "Anonymous"})

def show_login_page(request):
    return render_to_response('login.html', {})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

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
def notes_menu(request, note_id = None, sort=None):
    assert request.method == 'GET'
    if sort == "date":
        user_notes = Notes.objects.filter(owner = request.user).order_by("-last_edit")
    elif sort == "importance":
        user_notes = Notes.objects.filter(owner = request.user).order_by("importance")
    elif sort == "shared":
        user_notes = Notes.objects.filter(owner = request.user, shared_to = not None)
    else:
        user_notes = Notes.objects.filter(owner = request.user)
    if not note_id:
        try:
            note_id = user_notes[0].id
        except:
            pass
    return render_to_response('notes_menu.html', {'notes': user_notes, 
                                                  'note_id': note_id})
@login_required
def notes_list(request, note_id=None):
    assert request.method == 'GET'
    user_notes = Notes.objects.filter(owner = request.user)
    if not note_id:
        try:
            note_id = user_notes[0].id
        except:
            pass
    return render_to_response('notes_list.html', {'note_id': note_id})


@login_required
def notes_lists(request, note_id=None):
    return render_to_response('notes_lists.html', {})

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
            note = Notes(title = clean_data['title'], text = clean_data['text'], owner = request.user)
            note.save()
            note_id = str(note.id)
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
