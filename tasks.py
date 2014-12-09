import os
import time
from datetime import datetime

"""
upkeep
runs in the background of the server

updates reservation when they become active
sends messages to users if they haven't returned their tool on time

"""
def upkeep():
    while(True):
        now = datetime.now()
        tools = Tool.objects.all()
        for tool in tools:
            #go through all the tools and then get all reservations associated with those tools
            reservations = Reservation.objects.filter(is_complete=False, tool=tool, is_active=True, approved=True)
            if len(reservations) != 0:
                #this is the case where there is currently an active reservation for a tool
                for reservation in reservations:
                    if reservation.return_date < now:
                        #if the scheduled return date is less than now
                        if not reservation.message_sent:
                            #if there hasn't already been a notification sent
                            print(now.isoformat(' ') + " sending message to " + tool.borrower.username)
                            contents = "Your reservation has expired. Please return "+ reservation.owner.username +"'s "+ reservation.tool.name +"."
                            sender = get_object_or_404(ourUser, pk=tool.owner.id)
                            receiver = get_object_or_404(ourUser, pk=tool.borrower.id)
                            subject = "Expired Reservation"
                            message = Message(
                            date_sent=datetime.now(), subject=subject,
                            contents=contents, sender=sender, receiver=receiver,sent_by_system=True)
                            message.save()
                            reservation.message_sent = True
                            reservation.save()
            else:
                #from here we can assume the tool is not currently being borrowed
                reservations = Reservation.objects.filter(is_complete=False, tool=tool, approved=True, skipped=False)
                for reservation in reservations:
                    now = datetime.now()
                    if reservation.borrow_request_date <= now and reservation.return_date >= now:
                        #this is the case where there is no active reservation and this one fits the time slot
                        print(now.isoformat(' ') + " Activating reservation for " + tool.name)
                        reservation.is_active = True
                        reservation.save()
                        tool.borrower = reservation.borrower
                        tool.save()

                    elif reservation.borrow_request_date <= now and reservation.return_date <= now:
                        #this is the case when someone doesn't return their tool on time and a reservation is skipped
                        print(now.isoformat(' ') + " Skipping reservation for " + tool.name) 
                        reservation.skipped = True
                        reservation.is_complete = True
                        reservation.save()
                    else:
                        #this is the case where the reservation is still in the future
                        pass

        time.sleep(7)

if __name__ == "__main__":
    #set up the django environment for accessing the DB
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ToolShare.settings")
    #imports from the DB must be carried out after environment is set up
    from toolshareapp.models import Tool,Shed,Community,Reservation
    from userMessaging.models import Message
    from userManagement.models import ourUser
    from django.contrib.auth.models import User
    from django.shortcuts import get_object_or_404
    upkeep()
