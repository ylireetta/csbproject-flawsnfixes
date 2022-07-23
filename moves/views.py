import json
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

@login_required
def allmovesView(request):
    moves_list = Move.objects.all()
    context = {'move_list': moves_list}
    return render(request, 'moves/allmoves.html', context)

# CYBER SECURITY FIX (remove comment to fix flaw): Do not allow unauthenticated users to access page where new moves can be added to database
#@login_required
def addmoveView(request):
    if request.method == 'POST':
        new_move = Move.objects.create(move_name=request.POST.get('new_move_name'))
        return redirect('/moves')
    return render(request, 'moves/addmove.html')

def searchSessionsView(request):
    context = {}
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            parsed_date = datetime.datetime.strptime(request.POST.get('session_date'), '%Y-%m-%d')
            filtered_sessions = Session.objects.filter(date=parsed_date)
            context['sessions'] = filtered_sessions
            #return render(request, 'moves/searchmoves.html', context)
        except:
            # If parsing fails, no sessions are shown
            return render(request, 'moves/searchmoves.html')

    if Session.objects.all().count() > 0:
        latest_session = Session.objects.filter(owner=request.user).latest('id')
        session_moves = Set.objects.filter(session_id=latest_session)

        context['latest_session'] = latest_session
        context['session_sets'] = session_moves
        
        # Only latest session is shown as default
        return render(request, 'moves/searchmoves.html', context)
    
    return render(request, 'moves/searchmoves.html')


@csrf_exempt # this exempt would not be ok in production without replacement csrf protection
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

@csrf_exempt # this exempt would not be ok in production without replacement csrf protection
def saveSet(request):
    if request.method == 'POST':
        user_sessions = Session.objects.filter(owner=request.user, ended=False)
        if user_sessions.count() > 0:
            user_session_id = user_sessions.latest('id')

        else:
            user_session_id = Session.objects.create(owner=request.user, ended=False)

        #body = json.loads(request.body)
        #move_id = body.get('moveId', 0)
        #move = body.get('move', 'untitled')
        #move = Move.objects.get(id=move_id)
        #reps = body.get('reps', 0)
        #weights = body.get('weights', 0)

        # Get selected move id from dropdown list called 'moves'
        move_id = request.POST.get('moves')
        reps = request.POST.get('reps')
        weights = request.POST.get('weights')
        move = Move.objects.get(id=move_id)

        new_set = Set.objects.create(move_id=move, reps=reps, weight=weights, session_id=user_session_id)
        return JsonResponse({'set': new_set.id})

def saveSession(request):
    user_session = Session.objects.filter(owner=request.user).latest('id')
    user_session.ended = True
    user_session.save()
