from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from userMessaging.forms import *
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from userManagement.models import ourUser
from datetime import datetime
from ToolShare.decorators import loggedin
from django.contrib import messages

# view for sending a message

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

@loggedin
def send_message(request):
    #if the user has pressed submit (a post request)
    args = {}
    temp_user = ourUser.objects.get(username=request.user.username)
    args['user'] = temp_user
    if request.POST:
        form = user_messaging_form(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if temp_user == message.receiver: # so user can't send to their self
                form = user_messaging_form()
                args.update(csrf(request))
                args['form'] = form
                args['users'] = ourUser.objects.filter(community=temp_user.community).filter(is_active=True)
                args['warn'] = "You can't send a message to yourself"
                return render_to_response('send_message.html', args)
            else: #store the current user as the sender and the time sent as now
                message.create(temp_user)



                args['notify'] = 'You successfully sent a message to ' + message.receiver.username


                #supposed to make a success message appear
                messages.success(request, 'you sent a message to ' + message.receiver.username)

                args['form'] = form
                args['users'] = ourUser.objects.filter(community=temp_user.community)
                my_inbox = Message.objects.filter(receiver = temp_user) #filter inbox so user gets only message where they recieve
                args['messagesInbox'] = my_inbox #messages is avalible in template, is list in user's inbox
                args['name'] = "Inbox"
                return render(request,'mailbox.html',args)
        else: #ask user to fix error
            args.update(csrf(request))
            args['form'] = form
            args['users'] = ourUser.objects.filter(community=temp_user.community)
            return render_to_response('send_message.html', args)
    else: # if user needs to fill out form
        form = user_messaging_form()
        args.update(csrf(request))
        args['form'] = form
        args['users'] = ourUser.objects.filter(community=temp_user.community)
        return render_to_response('send_message.html', args)

#for viewing a single message
@loggedin
def view_message(request, message_id):
    args = {}
    message = get_object_or_404(Message, id=message_id)
    user = get_object_or_404(ourUser,id=request.user.id)
    if user == message.sender or user == message.receiver:
        message.read = True
        message.save()
        args['message'] = message
        args['user'] = user
        return render_to_response('view_message.html',args)
    else:
        args['user'] = user
        return render_to_response('401.html',args)

#for veing all messages sent to user
@loggedin
def inbox(request):
    user = get_object_or_404(ourUser, username = request.user.username)
    args = {}
    my_inbox = Message.objects.filter(receiver=user,deleted_receiver=False) #filter inbox so user gets only message where they recieve
    args['messagesInbox'] = my_inbox #messages is avalible in template, is list in user's inbox
    args['name'] = "Inbox"
    args['user'] = user
    return render(request,'mailbox.html',args)

#for viewing all messages that user sent
@loggedin
def sent_messages(request):
    user = get_object_or_404(ourUser, username=request.user.username)
    flag1 = "Your tool has been returned"
    flag2 = "Expired Reservation"
    flag3 = "User Community Change"
    args = {}
    my_inbox = Message.objects.filter(sender=user,deleted_sender=False).exclude(subject=flag1).exclude(subject=flag2).exclude(subject=flag3)
    args['messagesInbox'] = my_inbox #messages is avalible in template, is list in user's inbox
    args['name'] = "Sent Mail"
    args['user'] = user
    return render_to_response('mailbox.html',args)

@loggedin
def delete_message(request, message_id):
    user = get_object_or_404(ourUser,id=request.user.id)
    message = Message.objects.get(pk=message_id)
    message.delete_message(user)
    return HttpResponseRedirect('/user/inbox/')