from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import get_model
import datetime
from ToolShare.validators import validate_txt_feild

def validate_zipcode(value):
    if not value.isdigit():
        raise ValidationError('Zipcode must be a number')
    elif len(value) != 5:
        raise ValidationError('Zipcode must be length 5')

def validate_reputation(value):
    if value < 0:
        raise ValidationError('reputation must be greater than zero')
    elif value > 5:
        raise ValidationError('reputation must be less than five')

def validate_age(value):
    d = datetime.date.today()-datetime.timedelta(days=(16*365))
    print(value)
    print(d)
    if value > d:
        raise ValidationError('You are not old enough to use this website')

# Create your models here.

"""
Reputation
"""

class FeedBack(models.Model):
    user = models.ForeignKey('ourUser', related_name="user")
    rater = models.ForeignKey('ourUser', related_name="rater")
    reputation = models.IntegerField(validators=[validate_reputation])
    comment = models.CharField(max_length=200)
    is_active = models.BooleanField()

    def post(self, reservation,mess_id=None):
        #Reservation = get_model('toolshareapp', 'Reservation')
        ourUser = get_model('userManagement', 'ourUser')
        self.rater = get_object_or_404(ourUser,id=reservation.owner.id)
        self.user = get_object_or_404(ourUser,id=reservation.borrower.id)
        self.is_active = True
        reservation.feed_back_given=True
        reservation.save()
        self.save()
        if mess_id != None:
            Message = get_model('userMessaging','Message')
            message = get_object_or_404(Message,id=mess_id)
            message.delete_message(self.rater)

"""
User Class
"""

class ourUser(User):
    age = models.DateField(validators=[validate_age])
    community = models.ForeignKey('toolshareapp.Community', null=True)
    zipcode = models.CharField(max_length=5,validators=[validate_zipcode])
    address = models.CharField(max_length=200, validators=[validate_txt_feild])

    def __init__(self, *args, **kwargs):
        super(ourUser, self).__init__(*args,**kwargs)

    def is_comm_admin(self):
        if self.community.admin == self:
            return True
        else:
            return False

    def is_shed_admin(self):
        Shed = get_model('toolshareapp','Shed')
        sheds = Shed.objects.filter(community=self.community,admin=self)
        if sheds:
            return True
        elif self.community.admin == self:
            return True
        else:
            return False


    def join(self, community, tools, lent, reserved_tools, reservations):
        if tools:
            for tool in tools:
                tool.community = community
                tool.save()
        if lent:
            for res in lent:
                res.change_community()
        if reserved_tools:
            for tool in reserved_tools:
                tool.return_tool()
        if reservations:
            for reservation in reservations:
                reservation.is_active = False
                reservation.skipped = True
                reservation.save()
        self.community = community
        self.save()

    def switch_shed_admin(self):
        if self.community:
            Shed = get_model('toolshareapp','Shed')
            sheds = Shed.objects.filter(admin=self)
            for shed in sheds:
                shed.admin = self.community.admin
                shed.save()


    def switch_comm_admin(self):
        if self.community:
            if self.community.admin == self:
                users = ourUser.objects.filter(community=self.community).exclude(id=self.id)
                users.order_by('reputation')
                if users:
                    self.community.admin_change(users[0])
                else:
                    self.community.is_active = False
                    self.community.save()

    def reputation(self):
        feed = FeedBack.objects.filter(user=self)
        if len(feed) == 0:
            return 0
        else:
            counter = 0
            accum = 0
            for entry in feed:
                accum += entry.reputation
                counter += 1
            return float("{0:.2f}".format(accum/counter))

    def BANHAMMER(self):
        Tool = get_model('toolshareapp', 'Tool')
        Reservation = get_model('toolshareapp', 'Reservation')
        myTools = Tool.objects.filter(owner=self)
        for tool in myTools:
            reservations = Reservation.objects.filter(tool=tool)
            tool.remove(reservations)
        borroweredTools = Tool.objects.filter(borrower=self)
        for tool in borroweredTools:
            tool.return_tool()
        givenFeedBack = FeedBack.objects.filter(rater=self)
        for feed in givenFeedBack:
            feed.is_active = False
            feed.save()
        self.is_active = False
        self.save()

    def got_mail(self):
        Message = get_model('userMessaging', 'Message')
        Reservation = get_model('toolshareapp', 'Reservation')
        dat_mail = Message.objects.filter(read=False,receiver=self)
        dem_reservations = Reservation.objects.filter(owner=self,approved=False)

        if dat_mail:
            return True
        elif dem_reservations:
            return True
        else:
            return False




