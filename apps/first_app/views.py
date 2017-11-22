# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models

from models import *

def noname(req):
    return 'id' not in req.session

def index(req):
    return render(req, "first_app/index.html")

def login(req):
    result = User.manager.login(req.POST)
    if result[0]:
        req.session['id'] = result[1].id
        # print req.session['id']
        return redirect('/success')
    for message in result[1]:
        messages.error(req,message[1])
    return redirect('/')

def register(req):
    result = User.manager.createUser(req.POST)
    if result[0]:
        for key, message in result[1].iteritems():
            messages.error(req, message)
        return redirect('/')
    for key, message in result[1].iteritems():
        messages.error(req, message)
    return redirect('/')

def success(req):
    if noname(req):
        return redirect('/')
    user = User.manager.get(id=req.session['id'])
    allUser= User.manager.exclude(id=req.session['id'])
    friendships= user.friends.all()
    isUser = Friends.manager.filter(user=user)
    set1 = set(allUser)
    set2 = set()

    for friend in friendships: 
      # print friend.user.first_name
      set2.add(friend.friend)
    try: 
        friendships
    except Exception:
		friendships= {}
    try:
        # notFriends= allUser.exclude(id=req.session['id'])
        notFriends = set1 - set2
		# try new line with .add friends
    except Exception:
        notfriends={}

    if user.friends.exists():
    	numfriends=""
    	print numfriends
    else:
    	numfriends="You have no friends..."
    	print numfriends
    context= {
    	'numfriends': numfriends,
        'self': user,
        'friendships': friendships,
        'notFriends': notFriends,
        'user': User.manager.all()
    }
    if noname(req):
        return redirect('/')
    return render(req, "first_app/success.html", context)

def logout(req):
    req.session.flush()
    return redirect('/')

def user(req, id):
    user = User.manager.get(id=id)
    context= {
        'user':user
    }
    return render(req, 'first_app/user.html', context)

def join(req, id):
    otherperson= User.manager.get(id=id)
    currentuser=User.manager.get(id=req.session['id'])
    Friends.manager.create(user=currentuser, friend=otherperson) 
    return redirect('/success')

def remove(req, id):
    Friends.manager.get(id=id).delete()
    return redirect('/success')