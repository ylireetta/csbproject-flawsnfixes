from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Move

# Create your views here.
@login_required
def index(request):
    return render(request, 'moves/index.html')

@login_required
def allmovesView(request):
    moves_list = Move.objects.all()
    context = {'move_list': moves_list}
    return render(request, 'moves/allmoves.html', context)

def addmoveView(request):
    if request.method == 'POST':
        new_move = Move.objects.create(move_name=request.POST.get('new_move_name'))
        return redirect('/moves')
    return render(request, 'moves/addmove.html')


