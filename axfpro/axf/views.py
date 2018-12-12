from django.shortcuts import render, redirect
from . models import Wheel, Nav, mustbuy, Shop, MainShow, FoodTypes, Goods, User, Cart
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import time
import random
from django.conf import settings
import os



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


def market(request, categoryid, cid, sortid):
    leftSlider = FoodTypes.objects.all()
    if cid == "0":
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid, childcid=cid)

    group = leftSlider.get(typeid=categoryid)
    childList = []
    childnames = group.childtypenames
    arr1 = childnames.split("#")
    for str in arr1:
        arr2 = str.split(":")
        obj = {"childName": arr2[0], "childId": arr2[1]}
        childList.append(obj)

    cartlist = []
    token = request.session.get("token")
    if token:
        user = User.objects.get(userToken=token)
        cartlist = Cart.objects.filter(userAccount=user.userAccount)

    for p in productList:
        for c in cartlist:
            if c.productid == p.productid:
                p.num = c.productnum
                continue

    # sort
    if sortid == '1':
        productList = productList.order_by("productnum")
    elif sortid == '2':
        productList = productList.order_by("price")
    elif sortid == '3':
        productList = productList.order_by("-price")

    data = {
        "title": '闪送超市',
        "leftSlider": leftSlider,
        "productList": productList,
        "childList": childList,
        "categoryid": categoryid,
        "cid": cid,
    }
    return render(request, "axf/market.html", data)


def cart(request):
    data = {
        "title": '购物车',
    }
    return render(request, "axf/cart.html", data)


def changecart(request, flag):
    # 判断用户是否登录，用token
    token = request.session.get("token")
    # 如果为空，返回给前端js,让它判断后重新定向，此处不能用redirect
    if token == None:
        # 没登录
        return JsonResponse({"data": -1, "status": "error"})
    # 前端点击按钮传过来的商品id
    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    # 根据token判断出当前登录的哪个用户
    user = User.objects.get(userToken=token)

    if flag == '0':
        if product.storenums == '0':
            return JsonResponse({"data": -2, "status": "error"})
        # 根据用户id为条件取出改用户的购物车
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        # 判断购物车是否为空
        if carts.count() == 0:
           c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg, product.productlongname, False)
           c.save()
        else:
            try:
                # 如果不为空，通过传过来的商品id拿一下商品，看看购物车里面有没有
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum += 1
                c.productprice = "%.2f" % float(product.price * c.productnum)
                c.save()
            # 如果没有,添加进去
            except Cart.DoesNotExist as e:
                # 直接增加一个商品信息
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,
                                    product.productlongname, False)
                c.save()
                product.storenums -= 1
                return JsonResponse({"data":c.productnum, "status": "success"})


    elif flag == '1':
        # 根据用户id为条件取出改用户的购物车
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        # 判断购物车是否为空
        if carts.count() == 0:
            return JsonResponse({'data': -2, "status": 'error'})
        else:
            try:
                # 如果不为空，通过传过来的商品id拿一下商品，看看购物车里面有没有
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum -= 1
                c.productprice = "%.2f" % float(product.price * c.productnum)
                if c.productnum == 0:
                    c.delete()
                else:
                    c.save()
            # 如果没有,添加进去
            except Cart.DoesNotExist as e:
                return JsonResponse({'data': -2, "status": 'error'})
            product.storenums += 1
            product.save()
            return JsonResponse({"data":c.productnum, "status": "success"})
    elif flag == '2':
        pass
    elif flag == '3':
        pass

def mine(request):
    username = request.session.get("username", "未登录")
    data = {
        "title": '我的',
        "username": username,
    }
    return render(request, "axf/mine.html", data)




from . forms.login import LoginForm
from django.http import HttpResponse
def login(request):
    if request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():
            # 信息格式没多大问题，验证帐号和密码的正确性
            nameid = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            try:
                user = User.objects.get(userAccount=nameid)
                if user.userPasswd != pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                return redirect('/login/')

            # 登录成功
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session["username"] = user.userName
            request.session["token"] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'axf/login.html', {"title": "登录", "form": f, "error": f.errors})
    else:
        f = LoginForm()
        return render(request, 'axf/login.html', {"title": "登录", "form": f})



def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPass")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank = 0

        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)
        f = request.FILES["userImg"]
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + ".png")
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()

        request.session["username"] = userName
        request.session["token"] = userToken

        return redirect('/mine/')
    else:
        return render(request, 'axf/register.html', {"title": "注册"})


from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')


def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount = userid)
        return JsonResponse({"data":"改用户已经被注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"可以注册","status":"success"})

