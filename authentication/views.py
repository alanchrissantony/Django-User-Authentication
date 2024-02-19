from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages



# Create your views here.

def home(request):
    if 'username' in request.session:
        return render(request,"Youtube/index.html")
    return redirect('signin')

def roothome(request):
    if "admin" not in request.session:
        return redirect('root')
    myUser = User.objects.all()
    if request.method == "POST":
        key = request.POST['search']
        myUser = User.objects.filter(username__icontains=key)
    return render(request,"account/admin.html",{'users':myUser})

def login(request):
        if 'username' in request.session:
            return redirect('home')
        if request.method == "POST":
            email=request.POST['email']
            password=request.POST["pass"]

            user = authenticate(username=email, password=password)

            if user is not None:
                request.session['username']=str(user)
                return render(request,"Youtube/index.html")
            else:
                messages.success(request, "Invalid Credentials")
                return render(request,"account/login.html")
   
        return render(request,"account/login.html")

def root(request):
    if "admin" in request.session:
        return redirect("roothome")
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST["pass"]
        myUser = User.objects.filter(username=email).values('is_superuser')
        if len(myUser) > 0:
            myUser = myUser[0]
            if myUser['is_superuser']:
                user = authenticate(username=email, password=password)
                if user is not None:
                    request.session['admin']=str(user)
                    return redirect("roothome")
                else:
                    messages.success(request, "Invalid Credentials")
                    return render(request,"account/admin-login.html")
   
    return render(request,"account/admin-login.html")


def signup(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["pass"]
        repassword = request.POST["re_pass"]
        print(username)
        if password==repassword:
            try:
                myUser = User.objects.create_user(email, username, password)
                myUser.name = username
                myUser.save()
                messages.success(request, "Your account has been successfully created.")
                return redirect('signin')
            except Exception as error:
                messages.success(request, "User already exits")
                return redirect('signup')

            
        else:
            messages.error(request,"Password doesn't match")
    return render(request,"account/signup.html")

def signout(request):
    request.session.clear()
    return redirect('signin')

def edit(request, id):
    if "admin" not in request.session:
        return redirect('root')
    myUser = User.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        myUser.username = email
        myUser.email = username
        myUser.save()
        myUser = User.objects.all()
        return redirect("roothome")
    return render(request,"account/edit.html",{'users':myUser})

def delete(request, id):
    if "admin" not in request.session:
        return redirect('root')
    myUser = User.objects.get(id=id)
    myUser.delete()
    myUser = User.objects.all()
    return redirect("roothome")