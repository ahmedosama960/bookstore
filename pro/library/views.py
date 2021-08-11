from collections import Counter
from django.db.models import Count
from django.contrib import auth
from django.db.models.aggregates import Sum
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.functional import empty
from library import forms, decorators
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.db import connection
from library.models import *
from library.models import UserAddress

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    user=request.user
    book=Book.objects.get(pk=productId)
    order , created=UserOrder.objects.get_or_create(user=user,completed=False)
    OrderItem ,created=OrderItems.objects.get_or_create(order=order,book=book)

    if action == "add":
        OrderItem.quantity = (OrderItem.quantity +1)
    elif action =="remove":
         OrderItem.quantity = (OrderItem.quantity -1)
    OrderItem.save()
    if OrderItem.quantity <= 0:
        OrderItem.delete()
    
    order.get_cart_total
    print(order.get_cart_total)
    

    return JsonResponse({'totalCalo':order.get_cart_items},safe=False)

# we will use django filter to search for books by category and book_name
def main(request):
    books = Book.objects.all()
    context = {"books":books}
    return render(request,"books_list.html", context)

def cart(request):
    return render(request,'cart.html')


def address(request):
    if request.method=="POST":
        user = request.user
        city = request.POST.get('city')
        street = request.POST.get('street')
        building = request.POST.get('building')
        address_type =request.POST.get('address_type')
        phone=request.POST.get('phone')
        data=UserAddress.objects.create(user=user,city=city,street=street,building=building,address_type=address_type,phone=phone)
        data.save()
        return redirect("checkout")
    return render(request,'address.html')

@login_required(login_url="/login/")
def checkout(request):
    if request.method == "POST":
        user=request.user
        order=UserOrder.objects.get(user=user,completed=False)
        address_id=request.POST.get('address_id')
        address_data=UserAddress.objects.get(pk=address_id)
        order.address=address_data
        order.completed=True
        order.save()
        return redirect('myorder')
    return render(request,'check.html')

@login_required(login_url="/login/")
def myorder(request):
    order=UserOrder.objects.filter(user=request.user,completed=True)
    context={"orders":order}
    return render(request,'myorder.html',context)


def book_query(request, pk):
    """Query only 1 book that a user would like to see its details"""
    book   = Book.objects.get(pk = pk)
    try:
        self_review = BookReview.objects.get(user=request.user,book=book)
        reviews=BookReview.objects.filter(book=book)
        context = {"book":book, "book_review":reviews,'self_review':self_review}
        
    except:
        reviews=BookReview.objects.filter(book=book)
        if reviews is not None:
            context = {"book":book, "book_review":reviews,'self_review':""}
        else:
             context = {"book":book}
        
    return render(request,"book_detail.html",context)



def myorderdetail(request,pk):
    
    order=UserOrder.objects.get(pk=pk)
    items=order.orderitems_set.all()  
    context={"order":order,"items":items}
    return render(request,'order_detail.html',context)


def book_category(request,category):
    categ= BookCategory.objects.get(name=category)
    book = Book.objects.filter(category=categ)
    context = {"books":book}
    return render(request,"books_list.html", context)


def book_search_backend(request):
    search="-"
    if request.method == "POST":
        search=request.POST.get('searchfield')
        search =str(search)
        if search is empty:
            search="-"
        
        return redirect('searching',search)
    return HttpResponse('heeellllo')

def book_search(request,search):
    name=str(search)
    book = Book.objects.filter(title__contains=name)
    context = {"books":book}
    return render(request,"books_list.html", context)


@decorators.unauthenticated_user
def sign_up(request):
    """SignUp function, the decorators prevents access to login page while user is already loggedin"""
   
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        email =request.POST.get('email')
        try:
            user=LibraryUser.objects.create_user(username,password,email)
            user.set_password(password)
            user.save()
            messages.info(request, "Account created for " + username)
            user_log=authenticate(username=username,password=password)
            print(user_log)
            if user_log is not None : # the re authincticate
                login(request,user_log)
                return redirect("main")
        except:
            messages.info(request,"Account couldn't be created.")
            return redirect("sign_up")
    
    return render(request,"sign_up.html")


@decorators.unauthenticated_user
def user_login(request):
    """User login function, the decorators prevents access to login page while user is already loggedin"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("main")
        else:
            messages.info(request, "Username or Password is incorrect.")
            return redirect("login")
    return render(request,'login.html')


@login_required(login_url="login")
def user_logout(request):
    """Logging out by POST request (make a form of method POST in the html with action of the url)"""
    logout(request)
    return redirect("main")


@login_required(login_url="login")
def add_book_review(request):
    """Receiving review data sent by user from book_review.html"""
    book_id=request.POST.get('book_id')
    book = Book.objects.get(pk=book_id)
    
    if request.method == "POST":
        description = request.POST.get("description")
        rate = request.POST.get("rate")
        book_review = BookReview.objects.create(user=request.user,book=book,description=description,rate=rate)
        book_review.save()
        return redirect("book_detail",pk=book_id)
    return render(request, "book_review.html")



@login_required(login_url="login")
def delete_book_review(request, book_pk):
    try:
        book = Book.objects.get(pk=book_pk)
        book_review = BookReview.objects.get(user=request.user,book=book)
        if request.method == "POST":
            book_review.delete()
            return redirect("dashboard")
    except:
        pass

    return render(request,"delete_book_review.html")


# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
# Functions for Admin

# # @decorators.admin_only
def dashboard(request):
    """listing all books in admin dashboard page"""
    # there'll be add_book button in page that opens add_book page
    # for each book, there'll be update, delete button
    books = Book.objects.all()
    context = {"books":books}
    c=connection.cursor()
    c.execute("SELECT c.name name,b.title title,count(o.book_id) AS  count FROM library_BookCategory c,library_Book b, library_OrderItems o where c.id=b.category_id AND b.id=o.book_id GROUP BY 1,2 ORDER BY 3 DESC ")
    # c.execute("SELECT c.name,b.id,b.title title,count(o.book_id) AS  count FROM library_BookCategory c,library_Book b, library_OrderItems o,library_UserOrder u where b.id=o.book_id AND o.order_id=u.id AND c.id=b.category_id AND u.date BETWEEN '2021-06-03' AND '2021-05-31' GROUP BY 1 ORDER BY 3 DESC ")
    # cat_order_date=dictfetchall(c)
    cat_order=dictfetchall(c)
    print("*********1*********")
    print(cat_order)
    orders= UserOrder.objects.filter(completed=True).order_by()
    total_income=0
    for order in orders:  
        total_income+=order.get_cart_total
    total_order=0
    for order in orders:
        total_order+=1
    c.execute("SELECT u.id id,u.username name , count(o.id) AS total_order from library_LibraryUser u , library_UserOrder o where u.id =o.user_id AND o.completed=True GROUP BY 1 ORDER BY 3 DESC")
    user_ordering=dictfetchall(c)

    context = {"books":books,"cat_order":cat_order,"total_income":total_income,"total_order":total_order,"orders":orders,"user_ordering":user_ordering}
    return render(request,"dashboard.html", context)


# @decorators.admin_only
def add_book_category(request):
    """Only Admin can add category for books in DB"""
    form = forms.CategoryForm()
    if request.method == "POST":
        form = forms.CategoryForm(request.POST)
        form.save()
        messages.info(request, "Category is saved successfully.")
        return redirect("dashboard")

    return render(request, "add_book_category.html", {"category_form":form})


# # @decorators.admin_only
def add_books(request):
    """Only admin can add Books to DB"""
    form = forms.BookForm()
    if request.method == "POST":
        form = forms.BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Book is saved successfully.")
            return redirect("dashboard")

    return render(request, "add_book.html", {"book_form":form})

# # @decorators.admin_only
def update_book(request, pk):
    """Only admin can update book data in DB"""
    book = Book.objects.get(pk= pk)
    form = forms.BookForm(instance= book)
    if request.method == "POST":
        form = forms.BookForm(request.POST,request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.info(request, "Book has been successfully updated.")
            return redirect("update_book", pk=pk)
        else:
            messages.info(request, "Book couldn't be updated!")
            return redirect("update_book", pk=pk)
    context = {"book_form":form}
    return render(request, "add_book.html", context)


# # @decorators.admin_only
def delete_book(request, pk):
    """Only admin can update book data in DB"""
    book = Book.objects.get(pk= pk)
    book.delete()
    return redirect("dashboard")

def myorderdashboard(request,pk):
    user=LibraryUser.objects.get(pk=pk)
    order=UserOrder.objects.filter(user=user,completed=True)
    context={"orders":order}
    return render(request,'myorder.html',context)
