from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return render(request, 'crowd_reactions/index.html', {});
