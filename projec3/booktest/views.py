from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse('rong is a good man')

def number(request):
    return HttpResponse('rong is a handsome man')

def rong(request):
    return HttpResponse('rong ia a nice man')