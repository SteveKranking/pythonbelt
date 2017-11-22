# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import collections
import re
import bcrypt
import datetime

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[^a-zA-Z]+$')

def uni_str_dict(mydict):
    data={}
    for key, value in mydict.iteritems():
        data[key] = str(value)
    return data

class UserManager(models.Manager):
    def createUser(self, form):
        flag = False
        errors = []
        data = uni_str_dict(form)
        # now= str(datetime.datetime.now())
        if User.manager.filter(email = data['email']):
            flag = True
            errors.append(("used_email", "Email already registered."))
            return (False, collections.OrderedDict(errors))
        if len(data['first_name'])<2:
            flag = True
            errors.append(('first_name_length', "Your first name must be at least three characters long"))
        if len(data['last_name'])<2:
            flag = True
            errors.append(('last_name_length', "Your last name must be at least three characters long")) 
        
        for char in range(len(data['first_name'])):
            if NAME_REGEX.match(data['first_name'][char]):
                errors.append(('first_name_number', "No non letters are allowed in first name"))
                flag = True
                break    
        for char in range(len(data['last_name'])):
            if NAME_REGEX.match(data['last_name'][char]):
                errors.append(('last_name_number', "No non letters are allowed in last name"))
                flag = True
                break    
        if not EMAIL_REGEX.match(data['email']):
            errors.append(('email', "Email Invalid."))
            flag = True
        if not data['password']== data['confirm_password']:
            errors.append(('password', "Passwords do not match"))
            flag= True       
        # if now > birthday:
        #     errors.append(('date', "Birthday must be valid"))
        #     flag= True
        
        if flag:
            return (False, collections.OrderedDict(errors))
        new_user = self.create(first_name = data['first_name'],last_name = data['last_name'], email = data['email'], birthday= data['birthday'], password = bcrypt.hashpw(data['password'], bcrypt.gensalt()))
        errors.append(('success', "You are now registered! Try logging in!"))
        return(True, collections.OrderedDict(errors), new_user)
    
    def login(self, form):
        flag = False
        errors = []
        data = uni_str_dict(form)
        try:
            called_user = User.manager.get(email=data['email'])
        except Exception:
            flag=True  
            errors.append(("Taken_User", "Username is incorrect/already taken"))
            return (False, errors)
        if not bcrypt.checkpw(data['password'].encode(), called_user.password.encode()):
            flag= True
            errors.append(("password", "Password Incorrect"))

        if flag:
            return (False, errors)
        return(True, called_user)

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length= 20)
    email = models.CharField(max_length= 50)
    password = models.CharField(max_length= 255)
    birthday = models.DateTimeField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager= UserManager()
    def __repr__(self):
        return "User {} {} {}".format(self.first_name, self.last_name, self.email)

class Friends(models.Model):
    user = models.ForeignKey(User, related_name="friends", null = True)
    friend = models.ForeignKey(User, related_name="users", null= True)
    manager= UserManager()
