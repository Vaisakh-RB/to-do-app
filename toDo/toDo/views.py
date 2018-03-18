from django.shortcuts import render
from django.contrib import auth

import pyrebase

config = {
    'apiKey': "AIzaSyD66kJhDOmkKB11i4s5p84QLn2-kl4YXKU",
    'authDomain': "to-do-list-c8542.firebaseapp.com",
    'databaseURL': "https://to-do-list-c8542.firebaseio.com",
    'projectId': "to-do-list-c8542",
    'storageBucket': "to-do-list-c8542.appspot.com",
    'messagingSenderId': "855992800494"
}

firebase = pyrebase.initialize_app(config)
# initializing firebase auth for Authentication
firebase_auth = firebase.auth()
# initializing firebase database
firebase_database = firebase.database()


def login_method(request):
    message = "Please Login."
    return render(request, template_name='index.html', context={'message': message})


def post_login_credentials(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = firebase_auth.sign_in_with_email_and_password(email=email, password=password)
        session_id = user['idToken']
        # set this firebase idToken as request session
        request.session['uid'] = str(session_id)
    except:
        message = "Invalid Credentials, Please try once again."
        return render(request, template_name='index.html', context={'message': message})
    return render(request, 'dashboard.html', context={'email': email})


def logout(request):
    auth.logout(request)
    message = 'Work Hard and Have good intentions !'
    return render(request, template_name='index.html', context={'message': message})


def sign_up(request):
    message = "Work hard, stay positive, and get up early. It's the best part of the day."
    return render(request, 'signup.html', context={'message': message})


def save_user(request):
    user = None
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password'),
    mobile = 1234567890
    age = 24
    gender = 'Male'

    try:
        user = firebase_auth.create_user_with_email_and_password(email=email, password=password)
        message = "Successfully created the user. Please login"
    except:
        message = "Couldn't be able to complete the action. Please Try again after sometime."
    if user and firebase_database:
        # saving the unique localId as user id or primary key for identification.
        user_id = user.get('localId')
        # saving data in firebase model.
        user_details = {
            'name': name,
            'email': email,
            'password': password,
            'contact_mobile': mobile,
            'age': age,
            'gender': gender
        }
        firebase_database.child('users').child(user_id).child('details').set(data=user_details)
        return render(request, 'index.html', context={'message': message})
    return render(request, 'signup.html', context={'message': message})
