from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from . models import Grades, Students

def index(request):
    return HttpResponse('rong is a good man')

def number(request):
    return HttpResponse('rong is a handsome man')

def rong(request):
    return HttpResponse('rong ia a nice man')

def grades(request):
    # 去模板里取数据
    gradesList = Grades.objects.all()
    # 将数据传递给模板，模板再渲染页面，将渲染好的页面返回给浏览器
    return render(request, 'grades.html', {"grades": gradesList})


def students(request):
    studentsList = Students.objects.all()
    return render(request, 'students.html', {"students": studentsList})