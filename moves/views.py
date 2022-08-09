import json
from time import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Move, Session, Set
import datetime

# Create your views here.
@login_required
def index(request):
    return render(request, 'moves/index.html')

@login_required
def allmovesView(request):
    results = Move.objects.all() # Show all moves as default in the search view table
    moves_list = json.dumps(list(Move.objects.all().values()))
    
    # Live search
    if request.method == 'GET' and 'phrase' in request.GET:
        filtered_moves = list(Move.objects.filter(move_name__contains=request.GET.get('phrase')).values())
        return JsonResponse(filtered_moves, safe=False)

    # Flawed search that uses GET form: remove this to fix
    if 'search_by_phrase' in request.GET:
        results = addToContext(request, 'searchresults')

    # Fixed search that uses POST form
    if 'search_by_phrase' in request.POST:
        results = addToContext(request, 'searchresults')
    
    context = {
        'move_list': moves_list,
        'searchresults': results
    }
    return render(request, 'moves/allmoves.html', context)

@login_required
def addmoveView(request):
    if request.method == 'POST':
        Move.objects.create(move_name=request.POST.get('new_move_name'))
        return redirect('/moves')
    return render(request, 'moves/addmove.html')

@login_required
# CYBER SECURITY FIX 2: (rename this --> searchSessionsView) Use POST request to search for sessions completed on a specific date
def searchSessionsViewToRename(request):
    context = {}
    filtered_sessions = None
    latest_session = None
    session_moves = None
    if request.method == 'POST' and request.user.is_authenticated:
        if 'search_by_date' in request.POST:
            try:
                filtered_sessions = addToContext(request, 'sessions')
            except:
                # If parsing fails, no sessions are shown
                filtered_sessions = None
    try:
        latest_session, session_moves = addToContext(request, 'latest')
    except:
        latest_session = None

    context = {
        'sessions': filtered_sessions,
        'latest_session': latest_session,
        'session_sets': session_moves
    }
    
    return render(request, 'moves/searchsessions.html', context)

@login_required
# CYBER SECURITY FIX 2 (to fix: 1) rename this or remove completely AND 2) rename the method above): Use POST request instead of GET
def searchSessionsView(request):
    context = {}
    admin = None
    filtered_sessions = None
    latest_session = None
    session_moves = None
    # We need to check if the url contains get parameters - the method is also get when we navigate to this view as per usual
    if request.method == 'GET' and request.user.is_authenticated:
        if 'search_by_date' in request.GET:
            admin = addToContext(request, 'admin')
            try:
                filtered_sessions = addToContext(request, 'sessions')
            except:
                # If parsing fails, no sessions are shown
                filtered_sessions = filtered_sessions

    try:
        latest_session, session_moves = addToContext(request, 'latest')
    except:
        latest_session = latest_session

    context = {
        'admin': admin,
        'sessions': filtered_sessions,
        'latest_session': latest_session,
        'session_sets': session_moves
    }
    
    return render(request, 'moves/searchsessions.html', context)

# CYBER SECURITY FIX 5 (remove decorator to fix): when posting data, the views should require csrf token to be posted along with the actual data.
@csrf_exempt
def addSessionView(request):
    saveresult = ''
    session_id = None
    # https://stackoverflow.com/questions/59727384/multiple-django-forms-in-single-view-why-does-one-post-clear-other-forms
    if request.method == 'POST':
        if 'save_one_set' in request.POST:
            session_id = saveSet(request)
            saveresult = 'Set saved!'
        elif 'save_complete_session' in request.POST:
            saveSession(request)
            saveresult = 'Session saved!'
    moves_list = Move.objects.all()
    context = {
        'move_list': moves_list,
        'saveresult': saveresult,
        'session_id': session_id
    }
    return render(request, 'moves/addsession.html', context)

def saveSet(request):
    if request.method == 'POST':
        user_sessions = Session.objects.filter(owner=request.user, ended=False)
        if user_sessions.count() > 0:
            user_session_id = user_sessions.latest('id')

        else:
            user_session_id = Session.objects.create(owner=request.user, ended=False)

        # Get selected move id from dropdown list called 'moves'
        move_id = request.POST.get('moves')
        reps = request.POST.get('reps')
        weights = request.POST.get('weights')
        move = Move.objects.get(id=move_id)

        Set.objects.create(move_id=move, reps=reps, weight=weights, session_id=user_session_id)

        return user_session_id

def saveSession(request):
    user_session = Session.objects.filter(owner=request.user).latest('id')
    user_session.ended = True
    user_session.save()

@login_required
def deleteSession(request, id):
    # The url is something like localhost:8000/delete/1, so we get the id of the object to delete as parameter

    # CYBER SECURITY FIX 2: remove code on lines 161-165 and remove line comment on line 160 to check if the user who made the request is the owner of the training session to delete

    # fixedDelete(request, id)
    try:
        Session.objects.get(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, f'Session id {id} removed!')
    except:
        return redirect('/moves/searchsessions')

    return redirect('/moves/searchsessions')

def fixedDelete(request, id):
    try:
        session_to_delete = Session.objects.get(pk=id)

        if (session_to_delete):
            owner_user = session_to_delete.owner

            if request.user.username == owner_user:
                try:
                    Session.objects.get(pk=id).delete()
                    messages.add_message(request, messages.SUCCESS, f'Session id {id} removed!')
                except:
                    messages.add_message(request, messages.ERROR, f'Deleting session id {id} failed.')
            else:
                messages.add_message(request, messages.ERROR, f'You are not the owner of session id {id}.')
    except:
        messages.add_message(request, messages.ERROR, f'Deleting session id {id} failed.')

def addToContext(request, attribute):
    if attribute == 'sessions':
        # This will work regardless of whether we are using post or get method in the template form
        if request.method == 'POST':
            parsed_date = datetime.datetime.strptime(request.POST.get('session_date'), '%Y-%m-%d')
        elif request.method == 'GET':
            parsed_date = datetime.datetime.strptime(request.GET.get('session_date'), '%Y-%m-%d')
        
        filtered_sessions = Session.objects.filter(date=parsed_date)
        return filtered_sessions

    if attribute == 'searchresults':
        # This will work regardless of whether we are using post or get method in the template form
        if request.method == 'POST':
            phrase = request.POST.get('searchphrase')
        elif request.method == 'GET':
            phrase = request.GET.get('searchphrase')

        # The table for Move objects has been renamed to movestable in models.py
        # CYBER SECURITY FIX 4: queries should not be made with raw SQL and especially not by using placeholders in the SQL string.
        # Fix flaw 4 by using the following query method instead of raw SQL
        #results = Move.objects.filter(move_name__contains=phrase)
        
        results = Move.objects.raw("SELECT id, move_name FROM movestable WHERE move_name LIKE '%%%s%%'" % phrase)

        return results

    if attribute == 'admin':
        return request.GET.get('admin') == '1'

    if attribute == 'latest':
        latest_session = Session.objects.filter(owner=request.user).latest('id')
        session_moves = Set.objects.filter(session_id=latest_session)

        return latest_session, session_moves
    
def signupView(request):
    # CYBER SECURITY FIX 3: Remove the following code and use Django's own signup form instead
    form = None
    if request.method == 'POST':
        if 'signupform' in request.POST:
            new_username = request.POST.get('username')
            new_password = request.POST.get('password')
            new_email = request.POST.get('email')
            User.objects.create_user(new_username, new_email, new_password)
            return redirect('/moves')
        
        # Remove all following comments to fix flaw
        #if 'djangoform' in request.POST:
        #    form = UserCreationForm(request.POST)
        #    if form.is_valid():
        #        form.save()
        #        return redirect('/moves')
        #    else:
        #        messages.add_message(request, messages.ERROR, 'Please check instructions for username and password.')
        #        return redirect('/moves/signup')
    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})