from django import forms
from toolshareapp.models import *
from django.forms.extras.widgets import SelectDateWidget

#form used to interact with tools in the system, make and edit as well
class tool_form(forms.ModelForm):

    class Meta:
        model = Tool
        fields = ("name", "shed", "pickup_arrangements", "description")
    #makes the sheds only the sheds in the user's community
    def __init__(self, user=None, **kwargs):
        super(tool_form, self).__init__(**kwargs)
        if user:
            self.fields["shed"].queryset = Shed.objects.filter(community=user.community.id)

#form used to interact with sheds in the system, make and edit as well
class shed_form(forms.ModelForm):

    class Meta:
        model = Shed
        fields = ("name", "shed_address")

#form used to interact with communities in the system, and edit as well
class community_form(forms.ModelForm):

    class Meta:
        model = Community
        fields = ("name","zipcode",)

#form used to interact with reservations in the system, handled internally
class reservation_form(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("borrow_request_date", "return_date","reason",)



