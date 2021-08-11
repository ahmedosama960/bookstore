from django import forms
from library import models

class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.LibraryUser
        fields = ["username", "email", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }

class SignInForm(forms.ModelForm):
    class Meta:
        model = models.LibraryUser
        fields = ["username", "password"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.BookCategory
        fields = "__all__"

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"




