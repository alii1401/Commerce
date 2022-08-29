from ast import Delete
from dataclasses import field
from email import message
from itertools import product
from pydoc import describe
from select import select
from turtle import update
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import string
import re

from django.views import View

from .models import *


def index(request):
    product = Product.objects.filter(is_active = True)
    return render(request, "auctions/index.html", {
    "product":product
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password, email)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

global inf
def information(request, product_id):
    var = 0
    flag01 = 0
    inf = Product.objects.get(pk = product_id)
    bol = 0
    usd = int(inf.start_price) + 1
    # if request.user.is_authenticated:
    #     cur_bid = CurrentBid.objects.filter(username=request.user, listing = inf)
    #     flag01 = 1
    comment = Comment.objects.filter(listing = inf)

    inf_currents = CurrentBid.objects.filter(listing = inf)
    print(inf_currents)
    if inf_currents:
        li = []
        bol = 1
        for j in inf_currents:
            li += [j.current_bid]
            print(li)
            print("hello")
    # if li != []: 
        max_current = max(li)
        max_current += 1
        if max_current > usd :
                usd = max_current  
    # print(cur_bid)  

    if request.method == "POST" and 'remove_watchlist' in request.POST:
            print("hello")
            C = CurrentBid.objects.get(listing = inf)
            C.delete()
            # cur_bid = CurrentBid.objects.all()
            # print(cur_bid)
            bol = 0
            return render(request, "auctions/information.html",{
                "inf":inf,
                # "current_bid":current_bid,
                "var":var,
                "bol":bol,
                "usd":usd,
                "comments": comment
            })
        
    else:
        
        if request.method == "POST" and 'add_watchlist' in request.POST:
            price = int(request.POST.get("price"))
            # if flag00 == 1:
            if price < usd :
                    bol = 0
                    message = f"Your bid must be {usd} or more!"
                    return render(request,"auctions/information.html",{
                        "message":message,
                        "inf":inf,
                        "var":var,
                        "usd":usd,
                        "bol":bol,
                        "comments": comment
                    })
            # elif flag00 == 0 and price > usd:
            else:
                C = CurrentBid()
                C.username = request.user
                C.listing = inf
                C.current_bid = price 
                C.save()
                bol = 1
                # if inf.is_active == False :
                #     prices = CurrentBid.objects.filter
                current_bid = CurrentBid.objects.filter(username=request.user,listing=inf)

                return render(request, "auctions/information.html",{
                    "inf":inf,
                    "current_bid":current_bid,
                    "var":var,
                    "bol":bol,
                    "usd":usd,
                    "comments": comment
                })
            # elif flag00 == 0 and price <= usd:
            #     message = f"Your bid must be {usd} or more!"
            #     return render(request,"auctions/information.html",{
            #             "message":message,
            #             "inf":inf,
            #             "var":var,
            #             "usd":usd,
            #             "comments": comment
            #         })
        # elif request.method == "POST" and 'remove_watchlist' in request.POST:
        #     print("hello")
        #     C = CurrentBid.objects.get(listing = inf)
        #     C.delete()
        #     # cur_bid = CurrentBid.objects.all()
        #     # print(cur_bid)
        #     bol = 0
        #     return render(request, "auctions/information.html",{
        #         "inf":inf,
        #         "current_bid":current_bid,
        #         "var":var,
        #         "bol":bol
        #     })
        elif request.method == "POST" and 'close' in request.POST:

            P = Product.objects.get(id = product_id,is_active=True)
            P.is_active = False
            P.save(update_fields=['is_active'])
            
            return HttpResponseRedirect(reverse('auctions:index'))

        elif request.method == "POST" and 'add_comment' in request.POST:
            comment0 = request.POST["comment"]
            try:
                # comment = Comment.objects.filter()
                C = Comment() 
                C.username = request.user
                C.listing = inf
                C.comment = comment0
                C.save()
                return render(request, "auctions/information.html",{
                        "inf" : inf,
                        "usd" : usd,
                        "bol":bol,
                        "comments": comment
                        })
            except Exception :
                comment = Comment.objects.all()
                return render(request, "auctions/information.html",{
                        "inf" : inf,
                        "usd" : usd,
                        "bol":bol,
                        "comments": comment,
                        "message":"Error!"
                    })  

        # elif flag01 == 1:
        #     # bol = 0
        #     return render(request, "auctions/information.html",{
        #         "inf":inf,
        #         "var":var,
        #         "bol":bol,
        #         "usd":usd,
        #         "comments": comment
        #     })

        else:
                # inf = Product.objects.get(pk = product_id)
                # comment = Comment.objects.filter(listing=inf)
                return render(request, "auctions/information.html",{
                "usd" : usd,
                "inf":inf,
                "bol":bol,
                "comments":comment
            })
def create(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        group = request.POST.get('items')
        explain = request.POST["description"]
        price = request.POST["price"]
        url = request.POST["url"]

        P = Product()
        C = Category.objects.get(id = group)      
   
        P.username = request.user 
        P.category = C
        P.title = title
        P.description = explain
        P.start_price = price
        P.image = url
        P.save()
        message = "The product has been successfully registered."

        return render(request, "auctions/create.html",{
        "category" : category,
        "categories" : categories,
        "message":message
        })
            
        
    
    return render(request, "auctions/create.html",{
        "category" : category,
        "categories" : categories
        })

def watchlist(request):
    var = 0
    inf0 = CurrentBid.objects.all()
    temp = set()
    flag = 1
    # print(flag)
    
    # if inf0:
    for i in inf0 :
        # print( i.listing.is_active)
        if i.username == request.user and i.listing.is_active == True:
            # print("t")
            temp.add(i)
            # flag = 0
        # if flag == 0:
        #     return render(request, "auctions/watchlist.html",{
        #         "products":temp,
        #         "var":var
        #     })
    # oon product hayyi k harajishon tmom shodeh
    # inf1 = CurrentBid.objects.filter(is_active = False)
    
    # elif inf0 and flag == 1:
        # num = 0
    
    # temp1 = set()
    # message = ""
    # for j in inf0:
    #     li += [j.current_bid]
    # bishineh = max(li)
    # print(f"max={bishineh}")
    # print("test0") 
    flg = 0
    for i in inf0:
        li=[]
        if i.username == request.user and i.listing.is_active == False:
            # temp.add(i)
            inf_currents = CurrentBid.objects.filter(listing = i.listing)
            for j in inf_currents:
                li += [j.current_bid]
            bishineh = max(li)
            flg = 1
            if i.current_bid >= bishineh : 
                # print("test1")
                # num = i.current_bid
                message = f"You Gain {i.listing.title} !"
                flg = 1
            elif i.current_bid < bishineh:
                message = f"You Lose!{i.listing.title}"
                flg = 1
            else:
                var = 1
        else:
            var = 1
        # elif flg != 1:
        #     message = ""
            #     message = f"You equal!{i.listing.title}"
    # if  message:
    print(temp)
    # prices = CurrentBid.objects.filter(listing = inf,username=request.user)
    # l = len(inf)
    # for i in range(0,l):
    if flg == 1:  
        return render(request,"auctions/watchlist.html",{
                "message":message,
                "products":temp,
                "var":var
                    })
    else:
        return render(request,"auctions/watchlist.html",{
                "products":temp,
                "var":var
                    })

class listing(View):
    def get(self, request):
        categories = Category.objects.all()
        items = []
        for category in categories:
            items += [f"{category}"]
        return render(request, "auctions/categories.html",{
            "items":items
        })
    def post(self,request):
        wordlist=[]
        if request.method == "POST":
            category = request.POST.get('items',False)
            product = Product.objects.filter(is_active=True)
            
            for produc in product:
                if category == produc.category.category :
                    wordlist += [produc]

                
        if wordlist == [] :
            return render(request, "auctions/nmayesh.html",{
            "message":"This category has'nt any item! "
            })
        else:
            return render(request, "auctions/nmayesh.html",{
                        "wordlist":wordlist
                        })
