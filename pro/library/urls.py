from os import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from library import views

urlpatterns = [    

    path('',views.main,name="main"),
    path('updateItem/',views.updateItem,name="updateItem"),
    path("register/", views.sign_up,name="sign_up"),
    path("login/",views.user_login, name="login"),
    path("logout/",views.user_logout, name="logout"),
    path("book_detail/id=<int:pk>/", views.book_query, name="book_detail"),
    path('books/category=<str:category>/',views.book_category,name='category'),
    path('books/search_name=<str:search>/',views.book_search,name="searching"),
    path('book_search_backend/',views.book_search_backend,name="search_backend"),
    path("add_book_review/",views.add_book_review, name="add_book_review"),
    path('cart/',views.cart,name="cart"),
    path('check/',views.checkout,name="checkout"),
    path('address/',views.address,name="address"),
    path('myorders/',views.myorder,name="myorder"),
    path('myorders/order=<int:pk>',views.myorderdetail,name="myorderdetail"),
    
    # urls of admin:
    
    path("dashboard/",views.dashboard,name="dashboard"),
    path("dashboard/add_books/", views.add_books, name="add_books"),
    path("dashboard/update_book/<int:pk>/",views.update_book, name="update_book"),
    path("dashboard/delete_book/<int:pk>/", views.delete_book, name="delete_book"),
    path("dashboard/add_book_category/",views.add_book_category, name="add_book_category"),
    path('myorderdashboard/<int:pk>',views.myorderdashboard,name='myorderdashboard')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
