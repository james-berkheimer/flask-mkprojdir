from flask import Flask
from flask import request
import subprocess, os
from shutil import copyfile
from config import Config
from app import db
from app.models import User


ROOT_APP_DIR = Config.ROOT_APP_DIR

def getUsersDict():    
    userData = {}
    usersfile = ROOT_APP_DIR + "/users.txt"
    with open(usersfile, 'r') as file:
        for line in file:
            username = line.rstrip().split('@')[0].lower()
            userData[username] = line.rstrip().lower()
    return userData

def updateUsers():
    new_users = getUsersDict()
    current_users = User.query.all()
    for username, email in new_users.items():
        check_username = User.query.filter_by(username=username).first()
        check_email = User.query.filter_by(email=email).first()
        if check_username is None or check_username is None:
            print("Adding: " + username, email)
            user = User(username=username, email=email)
            user.set_password(username)
            db.session.add(user)
            db.session.commit()
        else:
            print("Users: " + username + " already exists")
    for user in current_users:
        if not checkKey(new_users, user.username):
            print("removing: " + user.username)
            db.session.delete(user)
            db.session.commit()

def checkKey(dict, key):       
    if key in dict.keys():
        return True
    else: 
        return False