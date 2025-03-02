from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date
# Create your views here.


def about(request):

    return render(request,'about.html')

def index(request):
    
    return render(request,'index.html')

def contact(request):
    
    return render(request,'contact.html')

def userlogin(request):
    error=""


    
    if request.method == 'POST':
        u=request.POST['emailid']
        p=request.POST['pwd']

        
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                
                # Check if the user exists in Signupstd
                signupstd_user = Signupstd.objects.filter(user__username=u).first()              
                if signupstd_user:
                    error = "no"  # User exists in Signupstd
                else:
                    signupteach_user = Signupteach.objects.filter(user__username=u).first()
                    # Check if the user exists in Signupteach
                    if signupteach_user:
                        return redirect('teach_profile')  # Redirect to teacher profile                    
            else:
                error = "yes"


        except Exception as e:
            error = str(e)     
    d={'error':error}
    return render(request,'login.html',d)

def login_admin(request):
    error=""
    if request.method =='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'login_admin.html',d)

def signup1(request):
    error=""
    if request.method=="POST":
            f=request.POST["firstname"]
            l=request.POST["lastname"]
            ro=request.POST["role"]
            y=request.POST["year"]
            rn=request.POST["rollno"]
            ti=request.POST["teachID"]
            b=request.POST["branch"]
            e=request.POST["emailid"]
            p=request.POST["pwd"]
            if ro=="student":
                try:
                    user=User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
                    Signupstd.objects.create(user=user,Rollno=rn,branch=b,year=y,role=ro)
                    error="no"
                except:
                    error="yes"
            elif ro=="teacher":
                try:
                    user=User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
                    Signupteach.objects.create(user=user,teachID=ti,branch=b,role=ro)
                    error="no"
                except:
                    error="yes"
    d={'error':error}    
    return render(request,'signup.html',d)

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    
    return render(request,'admin_home.html')

def std_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Signupstd.objects.get(user=user)
    notes=Notes.objects.filter(branch=data.branch)

    d={'data':data,'user':user,'notes':notes}
    return render(request,'std_profile.html',d)


def Logout(request):
    logout(request)

    return redirect('index')


def teach_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Signupteach.objects.get(user=user)
    notes=Notes.objects.filter(user=user)
    d={'data':data,'user':user,'notes':notes}   
    return render(request, 'teach_profile.html',d)

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=="POST":
            s=request.POST["subject"]
            n=request.FILES["notesfile"]
            f=request.POST["filetype"]
            d=request.POST["description"]
            u=User.objects.filter(username=request.user.username).first()
            data=Signupteach.objects.get(user=u)
            b=data.branch
            
            try:
                Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,
                subject=s,notesfile=n,fyletype=f,description=d,status='pending')                 
                error="no"
            except:
                error="yes"
            
    d={'error':error}
    
    return render(request,'upload_notes.html',d)

def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return  redirect('teach_profile')

