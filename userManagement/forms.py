from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from userManagement.models import ourUser, FeedBack
from django import forms

class user_create_form(UserCreationForm):
    

    class Meta:
        model = ourUser
        fields = ( "username", "zipcode", "address", "age" )

class user_update_form(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(user_update_form,self).__init__(*args,**kwargs)

    class Meta:
        model = ourUser
        fields = ( "zipcode", "address", )

class feed_back_form(forms.ModelForm):

    class Meta:
        model = FeedBack
        fields = ( "reputation", "comment")

class password_change_form(PasswordChangeForm):

    class Meta:
        model = ourUser
