from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from datetime import timedelta
from django.shortcuts import get_object_or_404
from userManagement.models import ourUser
from userMessaging.models import Message
from messageBoard.models import Post, communityWall
from ToolShare.validators import validate_txt_feild


def validate_zipcode(value):
    if not value.isdigit():
        raise ValidationError('Zipcode must be a number')
    elif len(value) != 5:
        raise ValidationError('Zipcode must be length 5')

"""
Community Class Stub
"""

class Community(models.Model):
    admin = models.ForeignKey('userManagement.ourUser',null=True, blank=True, related_name='comm_admin')
    zipcode = models.CharField(max_length=5,validators=[validate_zipcode])
    name = models.CharField(max_length=30,validators=[validate_txt_feild])
    is_active = models.BooleanField(default=True)

    def chain_mail(self, admin, user):
        contents = admin.username + " has updated your community."
        sender = get_object_or_404(ourUser,username=admin.username)
        receiver = get_object_or_404(ourUser, pk=user.id)
        subject = "Community changes"
        message = Message(
            date_sent=datetime.datetime.now(), subject=subject,
            contents=contents, sender=sender, receiver=receiver,sent_by_system=True)
        message.save()

    #returns in format name00000
    def __str__(self):
        return self.name

    #returns a list of all available tools in the community
    def list_available(self):
        tool_list = Tool.objects.filter(community=self.id, is_active=True)
        return list(tool_list)  # not sure what to return so just a list for now

    def make_community(self, user):
        self.admin = user
        self.save()
        user.community = self
        user.save()
        #create the Home shed that is present in all commuinties
        shed = Shed(community=self, name="Home", shed_address="Home", is_home=True)
        shed.save()
        community_wall = communityWall(wall_name=str(self.zipcode), community=self)
        community_wall.save()
        deleted = communityWall(wall_name="deleted", community=self, is_deleted=True)
        deleted.save()

    def admin_change(self,user):
        self.admin = user
        self.save()
        users = ourUser.objects.filter(community=self)
        for person in users:
            contents = user.username + " is now the admin of your community."
            sender = get_object_or_404(ourUser,username=user.username)
            receiver = get_object_or_404(ourUser, pk=user.id)
            subject = "admin changes"
            message = Message(
                date_sent=datetime.datetime.now(), subject=subject,
                contents=contents, sender=sender, receiver=receiver,sent_by_system=True)
            message.save()
        

 
"""
Tool Class
"""


class Tool(models.Model):
    name = models.CharField(max_length=50,validators=[validate_txt_feild])
    owner = models.ForeignKey('userManagement.ourUser', related_name='owner_id')
    borrower = models.ForeignKey('userManagement.ourUser', related_name='borrower_id', null=True, default=None,blank=True)
    shed = models.ForeignKey('Shed', null=True)
    description = models.CharField(max_length=200, unique=True,validators=[validate_txt_feild])
    is_active = models.BooleanField(default=True)
    community = models.ForeignKey('Community')
    pickup_arrangements = models.CharField(max_length=100, validators=[validate_txt_feild])

    def remove(self, res):
        if self.borrower:
            return False
        else:
            if len(res) != 0:
                for reservation in res:
                    reservation.skipped = True
                    contents = str(self.owner) + " has deactivated this tool: " 
                    sender = get_object_or_404(ourUser, pk=self.owner.id)
                    receiver = get_object_or_404(ourUser, pk=self.borrower.id)
                    subject = self.name + "has been deactivated."
                    message = Message(
                    date_sent=datetime.datetime.now(), subject=subject,
                    contents=contents, sender=sender, receiver=receiver,sent_by_system=True)
                    message.save()
                    reservation.save()
            self.is_active = False
            self.save()
            return True

    def activate(self):
        self.is_active = True
        self.save()

    def return_tool(self):
        reservation = get_object_or_404(Reservation, tool=self, is_active=True)
        sender = get_object_or_404(ourUser, pk=reservation.borrower.id)
        receiver = get_object_or_404(ourUser, pk=reservation.owner.id)
        subject = "Please provide feed back for " + sender.username + "."
        message = Message(
            date_sent=datetime.datetime.now(), subject=subject,
            contents="temp", sender=sender, receiver=receiver,sent_by_system=True)
        message.save()
        contents = self.name + " has been returned to you." + "\n" + "<p><a href='/user/feedBack/" + str(reservation.id) + "/" + str(message.id) + "/'>feed back</a></p>"
        message.contents = contents
        message.save()

        self.borrower = None
        self.save()

        
        reservation.is_active = False
        reservation.is_complete = True
        reservation.returned_on = datetime.datetime.now()
        reservation.save()
        
    def return_from_home(self,stats,mess_id=None):
        reservation = get_object_or_404(Reservation, tool=self, is_active=True)     
        if stats:
            self.return_tool()
            if mess_id != None:
                message = get_object_or_404(Message,id=mess_id)
                message.delete_message(self.owner)
        else:
            sender = get_object_or_404(ourUser, pk=self.borrower.id)
            receiver = get_object_or_404(ourUser, pk=self.owner.id)
            subject = "Your tool has been returned"
            message = Message(
            date_sent=datetime.datetime.now(), subject=subject, sender=sender, contents="temp",receiver=receiver,sent_by_system=True)
            message.save()
            message.contents = self.name + " has been returned to you. Please confirm that it has been returned." + "\n" + "<p><a href='/toolshare/approveReturn/" + str(reservation.id) + "/" + str(message.id) + "/'>approve</a></p>" 
            message.save()

            self.borrower = None
            self.save()

    def reserve(self, reservation, borrower):
        if self.shed.is_home:
            reservation.approved = False
            reservation.tool = self
            reservation.community = self.community
            reservation.borrower = borrower
            reservation.message_sent = False
            reservation.owner = self.owner
            reservation.is_active = False
            reservation.is_complete = False
            reservation.skipped = False
            reservation.save()
        else:
            reservation.approved = True
            reservation.tool = self
            reservation.community = self.community
            reservation.borrower = borrower
            reservation.message_sent = False
            reservation.owner = self.owner
            reservation.is_active = False
            reservation.is_complete = False
            reservation.skipped = False
            reservation.save()

    def create(self, user):
        self.owner = user
        user = get_object_or_404(ourUser,username=user.username)
        self.community = user.community
        self.save()

    def get_address(self, user):
        shed = self.shed
        if shed.is_home :
            #if it is use the users address instead of the sheds
            return self.owner.address
        else:
            #otherwise use the sheds address
            return shed.shed_address

    def is_admin(self, user):
        shed = self.shed
        comm = self.community
        if comm.admin.id == user.id:
            return True
        else: 
            if shed.admin:
                if shed.admin.id == user.id:
                    return True
            else:
                return False

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Tool, self).__init__(*args, **kwargs)

"""
Shed Class Stub
"""

class Shed(models.Model):
    admin = models.ForeignKey('userManagement.ourUser', null=True, blank=True)
    name = models.CharField(max_length=50, validators=[validate_txt_feild])
    community = models.ForeignKey('Community')
    shed_address = models.CharField(max_length=50, validators=[validate_txt_feild])
    is_home = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_tools(self):
        tools = Tool.objects.filter(shed=self,is_active=True)
        return tools

    def create(self, admin):
        self.admin = admin
        self.community = admin.community
        self.is_home = False
        self.save()


"""
Reservation Class
"""

class Reservation(models.Model):
    
    def validate_borrow(value):
        if value < (datetime.datetime.now()-timedelta(days=1)):
            raise ValidationError('Borrow date must be today or later.')

    def validate_return(value):
        if value < datetime.datetime.now():
            raise ValidationError('Return date must be after the current date.')

    def validate_availability(value):
        raise ValidationError('Tool is currently borrowed.')

    approved = models.BooleanField(default=False)
    tool = models.ForeignKey(Tool, null=True)
    community = models.ForeignKey('Community', null=True)
    borrow_request_date = models.DateTimeField(default=datetime.datetime.now())
    return_date = models.DateTimeField()
    returned_on = models.DateTimeField(null=True,blank=True,default=None)
    borrower = models.ForeignKey('userManagement.ourUser', related_name='borrower')
    message_sent = models.BooleanField(default=False)
    owner = models.ForeignKey('userManagement.ourUser', related_name='owner')
    is_active = models.BooleanField()
    is_complete = models.BooleanField(default=False)
    skipped = models.BooleanField(default=False)
    feed_back_given = models.BooleanField(default=False)
    reason = models.CharField(max_length=500,null=True,blank=True,default=None)


    def send_deny(self, content):
        sender = get_object_or_404(ourUser, id=self.owner.id)
        receiver = get_object_or_404(ourUser, id=self.borrower.id)
        subject = "tool request denied"
        contents = content
        message = Message(
            date_sent=datetime.datetime.now(), subject=subject,
            contents=contents, sender=sender, receiver=receiver)
        message.save()

    def send_accept(self):
        sender = get_object_or_404(ourUser, id=self.owner.id)
        receiver = get_object_or_404(ourUser, id=self.borrower.id)
        subject = "tool request accepted"
        contents = sender.username + " has accepted your request"
        message = Message(
            date_sent=datetime.datetime.now(), subject=subject,
            contents=contents, sender=sender, receiver=receiver,sent_by_system=True)
        message.save()

    def change_community(self):
        contents = self.owner.username + " has changed communities. Your reservation has been cancelled, please return the tool."
        sender = get_object_or_404(ourUser, pk=self.owner.id)
        receiver = get_object_or_404(ourUser, pk=self.borrower.id)
        subject = "User Community Change"
        message = Message(
            date_sent=datetime.datetime.now(), subject=subject,
            contents=contents, sender=sender, receiver=receiver,sent_by_system=True)
        message.save()


    #returns in format borrower_owner_datetime
    def __str__(self):
        return self.borrower.username + "_" + self.owner.username + "_" + \
            str(self.borrow_request_date)

    def __init__(self, *args, **kwargs):
        super(Reservation, self).__init__(*args, **kwargs)
"""
Statistics Class
"""

class Statistics(models.Model):
    community = models.ForeignKey('Community')

    def __init__(self, *args, **kwargs):
        super(Statistics, self).__init__(*args, **kwargs)
        self.community = args[0]

    #gets the most active attribute of a reservation in the database
    #gets called by generate using a list of fields
    #where the fields are the string names of reservation attributes
    #ex call: self.most_active_reservation(self, 'borrower') returns most active borrower

    def most_active_reservation(self, search_flag):
        #the dict holding the count of the flag in the db
        search_dict = {}
        #this is not necessary but hey
        flag = search_flag

        #all reservation objects
        res_plural = list(Reservation.objects.filter(approved=True))

        #if the list isn't empty...
        if len(res_plural) != 0:
            #iterate over every reservation in the db
            for res in res_plural:
                #if the flag is already in the dict, increment a counter
                if getattr(res, flag) in search_dict:
                    search_dict[getattr(res, flag)] += 1
                #otherwise add it to the dict and set initialize it to 1
                else:
                    search_dict[getattr(res, flag)] = 1

            most_active = max(search_dict, key=search_dict.get) #gets the key of the highest count
            #returns a list in format [key, value] of the most active
            most_active_list = []
            most_active_list.append(most_active) #= search_dict[most_active]
            most_active_list.append(search_dict[most_active])
            return most_active_list
        #otherwise return an empty list, duh
        return []

    #works pretty much the same as most_active_reservation
    #except it only gets the most active user for a community
    def most_active_poster(self):
        #gets the wall for the community
        self_wall = get_object_or_404(communityWall, community=self.pk,is_deleted=False)
        #search dictionary again, {poster:count}
        search_dict = {}
        posters = list(Post.objects.filter(wall=self_wall.id))
        #if there are posts
        if len(posters) != 0:
            for post in posters:
                if post.poster in search_dict.keys():
                    search_dict[post.poster] += 1
                else:
                    search_dict.update({post.poster: 0})
                    search_dict[post.poster] += 1
            #returns [poster, count] again
            most_active = max(search_dict, key=search_dict.get)
            most_active_list = []
            most_active_list.append(most_active)
            most_active_list.append(search_dict[most_active])
            return most_active_list
        return []

    #gets the 5 most recent reservations. Has to return a dict because django is being dumb
    def most_recent_res(self):
        most_recent_list = list(Reservation.objects.filter(community=self.community).filter(approved=True).order_by('-id')[:5])
        args = {}
        for i in range(len(most_recent_list)):
            args.update({i: most_recent_list[i]})

        return args


    #generates the stats for the community associated with the class
    def generate(self):
        #string params to be passed to most_active_reservation
        #THESE MUST BE RESERVATION ATTRIBUTE VARIABLE NAMES!!
        flags = ['owner', 'borrower', 'tool']

        #args to return for use in the view
        args = {}

        #iterate over the flags above and add it to args
        #in format {flag:[attribute, count]}
        for flag in flags:
            args[flag] = self.most_active_reservation(flag)
        #manually get the most active poster
        args['poster'] = self.most_active_poster()
        args['most_recent'] = self.most_recent_res()
        #this logic is iffy, but it seems to work. I'm not a logician
        #any(args) returns true if anything in the args has content,
        #so if not any(args) should be if there is not anything in the list
        if not any(args):
            return []
        #if there is anything:
        #append poster to flags and return the args to the view
        else:
            flags.append('poster')
            flags.append('most_recent')
            args['flags'] = flags
            return args
