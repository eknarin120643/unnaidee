from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect


def layout(request):
    if request.user.is_authenticated:
        user1 = UserUn.objects.get(email = request.user.username)
        countfav = user1.favorite.all().count()
        return {
            "name" : user1,
            "log": "logout",
            "countfav": countfav
            }
    return{"log": "login"}

def index(request):
    notebookall = NoteBook.objects.all()
    b = layout(request)
    b['notebookall']= notebookall
    return render(request,'notebook/index.html',b)


def about(request):
    return render(request,'notebook/about.html')

def register(request):
    return render(request,'notebook/register.html')

def addregister(request):
    if request.method == 'POST':
        name = request.POST['firstname']
        surname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if (name == '')and(surname == '')and(email == '')and(password == '')and(confirmpassword == ''):
            return render(request, "notebook/register.html", {
                "message": "Please assign information"
            })
        elif name == '':
            return render(request, "notebook/register.html", {
                "message": "Please assign Name"
            })
        elif surname == '':
            return render(request, "notebook/register.html", {
                "message": "Please assign Surname"
            })
        elif email == '':
            return render(request, "notebook/register.html", {
                "message": "Please assign Email address"
            })
        elif password == '':
            return render(request, "notebook/register.html", {
                "message": "Please assign Password"
            })
        else:
            if password == confirmpassword:
                userun = UserUn.objects.create(
                firstname = name,
                lastname = surname,
                email = email,
                password = password,
                )
                user = User.objects.create_user(
                username = email,
                password = password
                )
                userun.save()
                user.save()
                return render(request,'notebook/login.html')
            else:
                return render(request,'notebook/register.html', {
                    "message": "Confirm Password not correct"
                })
    return render(request,'notebook/register.html')

def login_logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'notebook/login.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "notebook/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "notebook/login.html")

def compare(request):
    b = layout(request)
    return render(request,'notebook/compare.html',b)

def favorite(request):
    if not request.user.is_authenticated:
        return render(request, "notebook/login.html")
    else:
        user1 = UserUn.objects.get(email = request.user.username)
        notebookallfav = user1.favorite.all()
        b = layout(request)
        b['notebookallfav']= notebookallfav
        return render(request,'notebook/favorite.html',b)
    return HttpResponseRedirect(reverse('index'))

def mark(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "notebook/login.html")
        else:
            idnotebook = request.POST["id"]
            user1 = UserUn.objects.get(email = request.user.username)
            notebook = NoteBook.objects.get(id = idnotebook )
            notebooks = user1.favorite.all()
            for x in notebooks:
                if x == notebook:
                    return HttpResponseRedirect(reverse('index'))
            user1.favorite.add(notebook)
            return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))

def unmarkfav(request):
    if request.method == "POST":
        idnotebook = request.POST["id"]
        user1 = UserUn.objects.get(email = request.user.username)
        notebook = NoteBook.objects.get(id = idnotebook)
        user1.favorite.remove(notebook)
        notebookallfav = user1.favorite.all()
        b = layout(request)
        b['notebookallfav']= notebookallfav
        return HttpResponseRedirect(reverse('favorite'),b)
    return HttpResponseRedirect(reverse('index'))

def notebook_page(request):
    if request.method == "POST":
        notebook_id = request.POST['notebook_id']
        notebook = NoteBook.objects.get(id = notebook_id)
        b = layout(request)
        b['notebook']= notebook
        return render(request,'notebook/notebookpage.html',b)
    return HttpResponseRedirect(reverse('index'))

def search(request):
    b = layout(request)
    input = request.POST['input']
    input = input.lower()
    notebookall = NoteBook.objects.all()
    notebooklist = []
    c = 0
    for notebook in notebookall:
        if notebook.search(input):
            notebooklist.append(notebook)
            c = c+1
    b['notebooklist']= notebooklist 
    b['c'] = c       
    return render(request,'notebook/search.html',b)
