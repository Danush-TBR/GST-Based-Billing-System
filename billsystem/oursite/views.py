from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User, auth
from .models import Stock

def home(request):
    if User.is_authenticated:
        Latest_Added_Stock=Stock.objects.order_by('-Recently_Updated')[0]
        if Latest_Added_Stock==None:
            return render(request,'oursite/home.html',dict())
        else:
            return render(request,'oursite/home.html',{'Last_Stock':Latest_Added_Stock})
    return render(request,'oursite/home.html',dict())
    # return HttpResponse("Hello Wolrd")
def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            print('Authenticated')
            return redirect("/")
        else:
            return render(request,'oursite/login.html',{"error_message":"Invalid Credentials"})
    else:
        return render(request,'oursite/login.html',dict())
    #return HttpResponse("This is a Login Page")
def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1=request.POST['password']
        password2=request.POST['password1']
        if User.objects.filter(username=username).exists():
            return render(request,"oursite/register.html",{'error_message':"User already Exists"})
        elif password1!=password2:
            return render(request,"oursite/register.html",{'error_message':"Password Mismatched"})
        else:
            user=User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name)
            user.save()
            return redirect("oursite:home")
    else:
        return render(request,template_name = "oursite/register.html")
def logout(request):
    auth.logout(request)
    return redirect('/')
def addStock(request):
    if User.is_authenticated:
        if request.method == 'POST':
            product_name=request.POST['product_name']
            No_of_Stocks=request.POST['no_of_stocks']
            New_Stock=Stock(Product_Name=product_name,No_of_stocks=No_of_Stocks,Date_Added=timezone.now(),Recently_Updated=timezone.now())
            New_Stock.save()
            #redirect(reverse('oursite:home', kwargs={'stock_data':"Stock Added Succesfully"}))
            # return HttpResponseRedirect(reverse('oursite:results', args=(question.id,)))
            return redirect("/",{'stock_data':"Stock Added Succesfully"})
            # return render(request,'oursite/home.html',{'stock_data':"Stock Added Succesfully"})
        return render(request,'oursite/addStock.html',dict())
    else: 
        return render(request,"oursite/register.html",{'error_message':"Login pannala bro neenga!"})
def removeStock(request):
    if request.method=='POST':
        try:
            Selected_Stock_id=request.POST['stock']
            #selected_stock=Stock.get(Product_Name="stock")
        except:
            Stocks=Stock.objects.all()
            return render(request,"oursite/removeStock.html",{'Stocks':Stocks,'error':"select a Stock"})
        else:
            Stock_To_Be_Removed=Stock.objects.get(id=Selected_Stock_id)
            Stock_To_Be_Removed.delete()
            return redirect('/')
    Stocks=Stock.objects.all()
    return render(request,"oursite/removeStock.html",{'Stocks':Stocks})