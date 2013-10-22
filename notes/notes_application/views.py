# Create your views here.
from forms import *
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from models import Notes, ConfirmEmail 
from django.utils.timezone import utc
import string, random, datetime

def user_with_email(user):
    if user.email:
        return True
    else:
        return False

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

def check_email(request):
    """
        View for redirecting users, which just has been logined.
    """
    if request.user.email:
        return HttpResponseRedirect('/notes_list/')
    else:
        return HttpResponseRedirect('/add_email/')

@login_required
def add_email(request):
    """
        Show add email page for GET request. Send email confirmation for POST request.
    """
    if request.method == 'GET':
        form = AddEmailForm
        return render_to_response('add_email.html', {'form': form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = AddEmailForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
            content = "http://semenov.ipq.co/confirm/" + confirmation_code
            send_mail(
                "Confirm registration",
                content,
                'notes.noreplay@gmail.com',
                [clean_data.get('email', 'noreply@example.com')],
                fail_silently=False
            )
            ConfirmEmail.objects.filter(user = request.user).delete()
            confirmation = ConfirmEmail(user = request.user, confirm_code = confirmation_code, email = clean_data['email']) 
            confirmation.save()
            return HttpResponseRedirect('/')
        return render_to_response('add_email.html', {'form': form}, context_instance=RequestContext(request))

def confirm_email(request, email_code):
    """
        This view calling, when user confirm email. If success email adding.
    """
    try:
        confirmation = ConfirmEmail.objects.get(confirm_code = email_code) 
    except:
        raise Http404
    if confirmation.date_created > (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1)):
        user = confirmation.user
        user.email = confirmation.email
        user.save()
        confirmation.delete()
    return HttpResponseRedirect('/notes_list/')

@login_required
@user_passes_test(user_with_email, login_url="/add_email/")
def edit_note(request, note_id=None):
    """
        View for adding or editing note.
    """
    if note_id:
        try:
            note = Notes.objects.get(owner = request.user, id = note_id)
            title = note.title
            text = note.text
            importance  = note.importance
        except:
            title = ""
            text = ""
        form = NoteForm(
            initial={'title': title, 'text': text, 'importance': importance}
        )
        return render_to_response('edit_note.html', {'form': form, 'note_id': note_id}, context_instance=RequestContext(request))
    else:
        form = NoteForm()
        return render_to_response('edit_note.html', {'form': form}, context_instance=RequestContext(request))

@login_required
@user_passes_test(user_with_email, login_url="/add_email/")
def notes_menu(request, note_id = None, sort=None):
    """
        Returns content fot notes_lists page. Loading by AJAX.
    """
    assert request.method == 'GET'
    if sort == "date":
        user_notes = Notes.objects.filter(owner = request.user).order_by("-last_edit")
    elif sort == "importance":
        user_notes = Notes.objects.filter(owner = request.user).order_by("-importance")
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
@user_passes_test(user_with_email, login_url="/add_email/")
def notes_list(request, note_id=None):
    """
        Return notes list for current user, without a sorting.
    """
    assert request.method == 'GET'
    user_notes = Notes.objects.filter(owner = request.user)
    if not note_id:
        try:
            note_id = user_notes[0].id
        except:
            pass
    return render_to_response('notes_list.html', {'note_id': note_id})

@login_required
@user_passes_test(user_with_email, login_url="/add_email/")
def notes_lists(request, note_id=None):
    """
        Show page with different sortings.
    """
    return render_to_response('notes_lists.html', {})

@login_required
@user_passes_test(user_with_email, login_url="/add_email/")
def save_note(request, note_id=None):
    assert request.method == 'POST' 
    form = NoteForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        if note_id:
            note = Notes.objects.get(owner = request.user, id = note_id)
            note.text = clean_data['text']
            note.title = clean_data['title']
            note.importance = clean_data['importance']
            note.save()
        else:
            note = Notes(title = clean_data['title'], text = clean_data['text'], owner = request.user, importance = clean_data['importance'])
            note.save()
            note_id = str(note.id)
        return HttpResponseRedirect('/note_content/' + note_id)

@login_required
@user_passes_test(user_with_email, login_url="/add_email/")
def note_content(request, note_id=None):
    if note_id:
        try:
            note = Notes.objects.get(owner = request.user, id = note_id)
        except:
            raise Http404
    return render_to_response('note_template.html', {'note_text': note.text, 'note_id': note_id, 'importance': note.importance})

@login_required
@user_passes_test(user_with_email, login_url="/add_email/")
def delete_note(request, note_id=0):
    try:
        note = Notes.objects.get(owner = request.user, id = note_id)
        note.delete()
    except:
        pass
    return HttpResponseRedirect('/notes_list/')
