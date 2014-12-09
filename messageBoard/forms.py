from django import forms
from messageBoard.models import Post, communityWall

#the form to make a community_wall and edit it as well
class communityWall_form(forms.ModelForm):

    #takes the communityWall class and uses it
    class Meta:
        model = Post
        fields = {'content', }

#the form used to make a post and interact with it
#in the system
class post_form(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("content",)
