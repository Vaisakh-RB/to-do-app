from django.shortcuts import render
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
auth = firebase.auth()


def login_method(request):
    return render(request, template_name='index.html')


def post_login_credentials(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = auth.sign_in_with_email_and_password(email=email, password=password)
    return render(request, 'dashboard.html', context={'email': email})

