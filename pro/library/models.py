from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.forms.fields import ImageField
# Create your models here.
 
class LibraryUser(AbstractUser):
    phone_number = models.CharField(max_length=18)

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    street = models.TextField(max_length=255)
    building = models.CharField(max_length=50)
    address_type = models.CharField(max_length=255)
    phone=models.CharField(max_length=14,null=True,blank=True)

    def __str__(self): 
        return f"[Adrres: {self.address_type} of User: {self.user}]"


class Role(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} Role: {self.role}"



class BookCategory(models.Model):
    name = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(BookCategory, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price =  models.FloatField()
    image=models.ImageField(upload_to='photos/%y/%m/%d',blank=True)

    def __str__(self):
        return self.title


class BookReview(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    rate = models.CharField(max_length=255)

    def __str__(self):
        return self.rate


class UserOrder(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE,blank=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)
    date=models.DateField(auto_now_add=True,blank=True,null=True)
    # total_price = models.FloatField()
    @property
    def get_cart_total(self):
        OrderItems=self.orderitems_set.all()
        total = sum([item.get_total for item in OrderItems])
        return total
    @property
    def get_cart_items(self):
        OrderItems=self.orderitems_set.all()
        total= sum([item.quantity for item in OrderItems])
        return total
    @property
    def get_items(self):
        OrderItems=self.orderitems_set.all()
        return OrderItems
    def __str__(self):
        return f"{self.user}"


class OrderItems(models.Model):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True ,blank=True,default=0)
    total_price = models.FloatField( null=True,blank=True,default=0)

    @property
    def get_total(self):
        total = self.quantity * self.book.price
        return total

    def __str__(self):
        return f"[Book: {self.book} of Order: {self.order}]"