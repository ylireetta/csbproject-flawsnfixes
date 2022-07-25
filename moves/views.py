from time import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import Move, Session, Set
import datetime

# Create your views here.
@login_required
def index(request):
    return render(request, 'moves/index.html')

# CYBER SECURITY FIX 2 (remove comment to fix flaw): Do not allow unauthenticated users to access page
#@login_required
def allmovesView(request):
    moves_list = Move.objects.all()
    context = {'move_list': moves_list}
    return render(request, 'moves/allmoves.html', context)

# CYBER SECURITY FIX 2 (remove comment to fix flaw): Do not allow unauthenticated users to access page
#@login_required
def addmoveView(request):
    if request.method == 'POST':
        new_move = Move.objects.create(move_name=request.POST.get('new_move_name'))
        return redirect('/moves')
    return render(request, 'moves/addmove.html')

# CYBER SECURITY FIX 2 (remove comment to fix flaw): Do not allow unauthenticated users to access page
#@login_required
# CYBER SECURITY FIX 3 (rename --> searchSessionsView): Use POST request to search for sessions completed on a specific date
def searchSessionsViewToRename(request):
    context = {}
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            parsed_date = datetime.datetime.strptime(request.POST.get('session_date'), '%Y-%m-%d')
            filtered_sessions = Session.objects.filter(date=parsed_date)
            context['sessions'] = filtered_sessions
        except:
            # If parsing fails, no sessions are shown
            return render(request, 'moves/searchsessions.html', context)

    try:
        latest_session = Session.objects.filter(owner=request.user).latest('id')
        session_moves = Set.objects.filter(session_id=latest_session)

        context['latest_session'] = latest_session
        context['session_sets'] = session_moves
        
    except:
        return render(request, 'moves/searchsessions.html', context)
    
    return render(request, 'moves/searchsessions.html', context)

# CYBER SECURITY FIX 3 (rename this or remove completely): Use POST request instead of GET
def searchSessionsView(request):
    context = {}
    # We need to check if the url contains get parameters - the method is also get when we navigate to this view as per usual
    if request.method == 'GET' and request.user.is_authenticated and request.GET.get('session_date'):
        if request.GET.get('admin') == '1':
            context['admin'] = True
        try:
            parsed_date = datetime.datetime.strptime(request.GET.get('session_date'), '%Y-%m-%d')
            filtered_sessions = Session.objects.filter(date=parsed_date)
            context['sessions'] = filtered_sessions
        except:
            # If parsing fails, no sessions are shown
            return render(request, 'moves/searchsessions.html', context)

    try:
        latest_session = Session.objects.filter(owner=request.user).latest('id')
        session_moves = Set.objects.filter(session_id=latest_session)

        context['latest_session'] = latest_session
        context['session_sets'] = session_moves
        
    except:
        return render(request, 'moves/searchsessions.html', context)
    
    return render(request, 'moves/searchsessions.html', context)

def addSessionView(request):
    # https://stackoverflow.com/questions/59727384/multiple-django-forms-in-single-view-why-does-one-post-clear-other-forms
    if request.method == 'POST':
        if 'save_one_set' in request.POST:
            saveSet(request)
        elif 'save_complete_session' in request.POST:
            saveSession(request)
    moves_list = Move.objects.all()
    context = {'move_list': moves_list}
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

def saveSession(request):
    user_session = Session.objects.filter(owner=request.user).latest('id')
    user_session.ended = True
    user_session.save()

# CYBER SECURITY FIX 2 (remove comment to fix flaw): Do not allow unauthenticated users to access page
#@login_required
def deleteSession(request, id):
    # The url is something like localhost:8000/delete/1, so we get the id of the object to delete as parameter
    try:
        Session.objects.get(pk=id).delete()
    except:
        return redirect('/moves/searchsessions')

    return redirect('/moves/searchsessions')