from django.db import models
import re

# Create your models here.


class UserManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        # Missing fields
        if post_data["first_name"] == "" or post_data["last_name"] == "" or post_data["email"] == "" or post_data["password"] == "":
            errors["empty_field"] = "One or more fields are empty."
        # Email syntax
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data["email"]):
            errors["email"] = "Email is invalid."
        # Email already exists
        user_list = User.objects.filter(email=post_data["email"])
        if len(user_list) > 0:
            errors["email_unique"] = "Email already exists."
        # Password length < 8
        if len(post_data["password"]) < 8:
            errors["password_length"] = "Password must be at least 8 characters."
        # Confirm password
        if post_data["password"] != post_data["confirm_pw"]:
            errors["confirm_pw"] = "Password does not match."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class WishManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        # Missing fields
        if post_data["name"] == "" or post_data["description"] == "":
            errors["empty_field"] = "One or more fields are empty."
        # Character length < 3
        if len(post_data["name"]) < 3 or len(post_data["description"]) < 3:
            errors["character_length"] = "Wish and description must both be at least 3 characters."
        return errors


class Item(models.Model):
    name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()


class Wish(models.Model):
    item = models.ForeignKey(Item, related_name="wishes")
    description = models.CharField(max_length=60)
    user = models.ForeignKey(User, related_name="wishes")
    granted_date = models.DateField()
    likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
