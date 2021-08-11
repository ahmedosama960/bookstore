from django.contrib import admin
from library.models import LibraryUser, UserAddress, UserRole, Role, UserOrder
from library.models import Book, BookCategory, BookReview, OrderItems
# Register your models here.
admin.site.register(LibraryUser)
admin.site.register(UserAddress)
admin.site.register(UserRole)
admin.site.register(Role)
admin.site.register(UserOrder)
admin.site.register(Book)
admin.site.register(BookCategory)
admin.site.register(BookReview)
admin.site.register(OrderItems)