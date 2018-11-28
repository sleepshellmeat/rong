from django.shortcuts import render
from . models import Wheel, Nav, mustbuy, Shop, MainShow
# Create your views here.
from django.http import HttpResponse



def home(request):
    wheelsList = Wheel.objects.all()
    navList = Nav.objects.all()
    mustbuyList = mustbuy.objects.all()

    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    mainList = MainShow.objects.all()
    data = {
        "title": '主页',
        "wheelsList": wheelsList,
        "navList": navList,
        "mustbuyList": mustbuyList,
        "shop1": shop1,
        "shop2": shop2,
        "shop3": shop3,
        "shop4": shop4,
        "mainList": mainList,

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