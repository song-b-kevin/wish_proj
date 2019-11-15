from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
import bcrypt
from .models import *

# Create your views here.


def index(request):
    return render(request, "wish_app/index.html")


def register(request):
    # Validation
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    # Hash password
    hashed_password = bcrypt.hashpw(
        request.POST["password"].encode(), bcrypt.gensalt())
    # Create user
    new_user = User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=hashed_password
    )
    # User session
    request.session["uid"] = new_user.id
    return redirect("/wishes")


def login(request):
    # Validation
    user_list = User.objects.filter(email=request.POST["email"])
    if len(user_list) > 0:
        if bcrypt.checkpw(request.POST["password"].encode(), user_list[0].password.encode()):
            request.session["uid"] = user_list[0].id
            return redirect("/wishes")
    messages.error(request, "Invalid email and/or password.",
                   extra_tags="login")
    return redirect("/")


def logout(request):
    request.session.clear()
    return redirect("/")


def wish_list(request):
    if "uid" in request.session:
        user = User.objects.get(id=request.session["uid"])
        context = {
            "user": user,
            "wish_list": user.wishes.filter(granted_date="0001-01-01"),
            "granted_list": Wish.objects.exclude(granted_date="0001-01-01")
        }
        return render(request, "wish_app/wish_list.html", context)
    return redirect("/")


def wish_stats(request):
    if "uid" in request.session:
        user = User.objects.get(id=request.session["uid"])
        context = {
            "user": user,
            "all_granted": len(Wish.objects.exclude(granted_date="0001-01-01")),
            "granted_wishes": len(user.wishes.exclude(granted_date="0001-01-01")),
            "pending_wishes": len(user.wishes.filter(granted_date="0001-01-01"))
        }
        return render(request, "wish_app/wish_stats.html", context)
    return redirect("/")


def wish_new(request):
    if "uid" in request.session:
        context = {
            "user": User.objects.get(id=request.session["uid"]),
        }
        return render(request, "wish_app/wish_new.html", context)
    return redirect("/")


def wish_create(request):
    # Validation
    errors = Wish.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wishes/new")
    # Check if item exists
    item_list = Item.objects.filter(name=request.POST["name"])
    if len(item_list) == 1:
        item = Item.objects.get(name=request.POST["name"])
    else:
        item = Item.objects.create(name=request.POST["name"])
    new_wish = Wish.objects.create(
        item=item,
        description=request.POST["description"],
        user=User.objects.get(id=request.session["uid"]),
        granted_date="0001-01-01"
    )
    return redirect("/wishes")


def wish_edit_page(request, wish_id):
    if "uid" in request.session:
        context = {
            "user": User.objects.get(id=request.session["uid"]),
            "wish": Wish.objects.get(id=wish_id)
        }
        return render(request, "wish_app/wish_edit.html", context)
    return redirect("/")


def wish_edit_db(request):
    # Validation
    errors = Wish.objects.validator(request.POST)
    wish_id = request.POST["wish_id"]
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/wishes/edit/{wish_id}")
    wish = Wish.objects.get(id=wish_id)
    wish.item.name = request.POST["name"]
    wish.description = request.POST["description"]
    wish.save()
    wish.item.save()
    return redirect("/wishes")


def wish_remove(request, wish_id):
    Wish.objects.get(id=wish_id).delete()
    return redirect("/wishes")

def wish_grant(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.granted_date = date.today()
    wish.save()
    return redirect("/wishes")

def wish_like(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session["uid"])
    wish.likes.add(user)
    return redirect("/wishes")

def wish_unlike(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session["uid"])
    wish.likes.remove(user)
    return redirect("/wishes")