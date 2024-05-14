from django import forms 
from .models import Customer, credit, CustomerReview

GenderChoice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )
class RawCustomerData(forms.ModelForm):
    person_id = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Personal ID", "class":"form-control"}), label="")
    personName = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Full Name", "class":"form-control"}), label="")
    phoneNumber = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
    gender = forms.ChoiceField(choices=GenderChoice,required=True, label="")
    cusAddress = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    postCode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Postcode", "class":"form-control"}), label="")
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Username", "class":"form-control"}), label="")
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
 		    model = Customer
 		    fields = ['person_id', 'personName', 'phoneNumber','gender','cusAddress','email','postCode', 'username', 'password']
                     
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model


# class userRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")

#     class Meta:
#             model = get_user_model()
#             fields = ['username', 'email', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super(userRegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()

#         return user

class Deposit(forms.ModelForm):
    balance = forms.DecimalField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Deposit", "class":"form-control"}), label="")

    class Meta:
            model = credit
            fields = ['balance']

class BankAcc(forms.ModelForm):
    creditNumber = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Credit Number", "class":"form-control"}), label="")
    balance = forms.DecimalField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Deposit", "class":"form-control"}), label="")

    class Meta:
            model = credit
            fields = ['creditNumber', 'balance']

RatingChoice = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
class Review(forms.ModelForm):
    #reviewID = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Credit Number", "class":"form-control"}), label="")
    content = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Write Your Comment here: ", "class":"form-control"}), label="")
    rating = forms.ChoiceField(choices=RatingChoice,required=True, label="")

    


    class Meta:
            model = CustomerReview
            fields = ['content', 'rating']

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Search something: ", "class":"form-control"}), label="")

class AmountOrdered(forms.Form):
    amount = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Num", "class":"form-control"}), label="")


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label="Docx File", widget=forms.ClearableFileInput(attrs={
          'class' : 'form-control'
    }))
    header = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Header ", "class":"form-control"}), label="")
    author = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"Author ", "class":"form-control"}), label="")
    titlePhoto = forms.ImageField(label="Title Image", widget=forms.ClearableFileInput(attrs={
          'class' : 'form-control'
    }))