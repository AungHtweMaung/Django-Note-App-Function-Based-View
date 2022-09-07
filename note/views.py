from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Note
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import NoteForm, CategoryForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required(login_url='login')
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_note")
    else:
        form = CategoryForm()
    return render(request, "create_category.html", {
        "form": form
    })

@login_required(login_url='login')
def create_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.user_id = request.user.id
            note.save()
            return redirect("dashboard")
    else:
        form = NoteForm()
    return render(request, "create_note.html", {
        "form": form,
    })

@login_required(login_url='login')
def edit_note(request, id):
    note = get_object_or_404(Note, pk=id)

    if note.user != request.user:
        return render(request, "components/error.html")
    else:
        if request.method == "POST":
            form = NoteForm(request.POST, instance=note)
            print(request.POST)
            if form.is_valid():
                form.save()

                return redirect("dashboard")
        else:
            form = NoteForm(instance=note)
    return render(request, "edit_note.html", {
        "form": form,
    })

@login_required(login_url='login')
def delete_note(request, id):
    note = get_object_or_404(Note, pk=id)

    if note.user == request.user:
        if request.method == "POST":
            note.delete()
            return redirect("dashboard")
    return redirect("dashboard")


@login_required(login_url='login')
def note_detail(request, id):
    note = Note.objects.filter(pk=id, user=request.user).first()
    print(note)
    return render(request, "note_detail.html", {"note": note})

@login_required(login_url='login')
def dashboard(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, "dashboard.html", {
        "notes": notes,
    })

# @login_required(login_url='login')
def signup(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Username, email or password can't be blank!
        if username=="" or email=="" or password=="":
            return render(request, "signup.html", {
                "error": "Username, email or password can't be blank!"
            })
            
        # Not allowed duplicate username and email
        email_already_exist = User.objects.filter(email=email).first()
        if email_already_exist != None:
            return render(request, "signup.html", {
                "error": "Email already used"
            })

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect("login")
        except IntegrityError as error:
            return render(request, "signup.html", {
                "error": "Username already exists",
            })
        
        # user.save()
    return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user != None:
            auth_login(request, user)
            return redirect("dashboard")

        else:
            return render(request, "login.html", {
                "error": "Username or password is invalid!"
            })

    return render(request, "login.html")

@login_required(login_url='login')
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("home")