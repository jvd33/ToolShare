from django.db import models
from django.contrib.auth.models import User
import datetime
from ToolShare.validators import validate_txt_feild



# message model describes what a message is
class Message(models.Model):
    date_sent = models.DateTimeField('Date sent')
    subject = models.CharField('Subject', max_length=100, validators=[validate_txt_feild])
    contents = models.TextField(max_length=1000 ,validators=[validate_txt_feild])
    sender = models.ForeignKey('userManagement.ourUser', related_name = 'sender') # connects a message to the sender user
    receiver = models.ForeignKey('userManagement.ourUser', related_name = 'receiver', null=True) # conntects a message to receiver usser
    read = models.BooleanField(default=False)
    sent_by_system = models.BooleanField(default=False)
    deleted_sender = models.BooleanField(default=False)
    deleted_receiver = models.BooleanField(default=False)
    #represents a message as it's subject
    def __str__(self):
        return self.subject

    def create(self, ourUser):
        self.sender = ourUser
        self.date_sent = datetime.datetime.now()
        self.save()

    #since we tie messages to the user and not to a mailbox, i'm just setting the receiver to null
    def delete_message(self,user):
        if user == self.sender:
            self.deleted_sender = True
            self.save()
        else:
            self.deleted_receiver = True
            self.save()



