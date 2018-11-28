from django.shortcuts import render
from . models import Wheel
# Create your views here.
from django.http import HttpResponse



def home(request):
    wheelsList = Wheel.objects.all()
    data = {
        "title": '主页',
        "wheelsList": wheelsList,
    }
    return render(request, "axf/home.html", data)


def market(request):
    data = {
        "title": '闪送超市',
    }
    return render(request, "axf/market.html", data)


def cart(request):
    data = {
        "title": '购物车',
    }
    return render(request, "axf/cart.html", data)


def mine(request):
    data = {
        "title": '我的',
    }
    return render(request, "axf/mine.html", data)