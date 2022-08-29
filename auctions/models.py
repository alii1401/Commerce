from asyncio.windows_events import INFINITE
from datetime import datetime
from time import timezone
from re import T
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    # user0 = models.CharField(max_length=64)
    # email    = models.CharField(max_length=40)
    # password = models.CharField(max_length=8)
    
    def __str__(self):
        return f"{self.username}"
    
    def __len__(self):
        return len(self.username)



class Category(models.Model):
    category = models.CharField(max_length = 255, null=True)
    # slug = models.SlugField(max_length = 255)

    def __str__(self):
        return self.category

    def __len__(self):
        return len(self.category)

    def add(self, item):
        self.category = item
        return self.category



class Product(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)
    title = models.CharField(max_length = 255)
    image = models.TextField(max_length=INFINITE, null=True, blank=True )
    # file = models.FileField(null = True, blank = True)
    start_price = models.PositiveIntegerField(default = '0')
    # your_price = models.PositiveIntegerField(default = '0')
    # slug = models.SlugField(max_length = 255, unique = True)
    description = models.TextField()
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.username}, title: {self.title}, category: {self.category}, description: {self.description}, start_price: {self.start_price} " 

    # def add(self, item):
    #     self.list.append(item)
    def add(self, item):
        self.category = item
        return self.category

class CurrentBid(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    current_bid = models.PositiveIntegerField(null=True ,blank=True )

    def __str__(self):
        return f"username:{self.username}:({self.current_bid}), listing:{self.listing}"

class Comment(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    def __str__(self):
        return f"{self.username}, {self.comment}"
