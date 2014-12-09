from django.shortcuts import render, render_to_response
from django.views import generic
from userManagement.forms import *
from messageBoard.forms import post_form
from userManagement.models import ourUser, FeedBack
from toolshareapp.models import Tool
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from toolshareapp.models import Community, Reservation, Shed
from django.shortcuts import get_object_or_404
from userMessaging.models import Message
from messageBoard.models import communityWall, Post
import datetime
from django.views.generic.edit import UpdateView
from ToolShare.decorators import loggedin
from django.template import RequestContext


from django.contrib import messages

# Create your views here.




MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'



def login_view(request):
    variable = messages.get_messages(request)
    for message in variable:
        print(message)
    state = "Log in:"
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "Log in successful!"
                request.session['user'] = user.id
                user = get_object_or_404(ourUser, username=request.user.username)
                if user.community:
                    return HttpResponseRedirect('/user/home')
                else:
                    return HttpResponseRedirect('/toolshare/select')
            else:
                state = "Error. Inactive account."
        else:
            state = "Incorrect username and/or password."
    args = {}
    args.update(csrf(request))
    args.update({'state':state, 'username':username})
    return render(request,'login.html',args)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    args = {}
    if request.POST:
        form = user_create_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.zipcode.isdigit():


                #create a success notification after redirecting
                messages.success(request,'You have registered as ' + user.username)
                user.save()
                return HttpResponseRedirect('/user/login')
            else:

                args.update(csrf(request))

                args['form'] = form
                args['zip'] = 1

                return render_to_response('register.html', args)
        else:
            args.update(csrf(request))

            args['form'] = form
            args['error'] = 1

            return render_to_response('register.html', args)
    else:
        form = user_create_form()

        args.update(csrf(request))

        args['form'] = form

        return render_to_response('register.html', args)
@loggedin
def home_view(request):
    args = {}
    args['user'] = get_object_or_404(ourUser,id=request.user.id)
    if request.POST:
        form = post_form(request.POST)
        if form.is_valid():
            #tie the post to the wall and define the user for the post
            user = get_object_or_404(ourUser, username=request.user.username)
            community_wall = list(communityWall.objects.filter(community=user.community).exclude(wall_name="deleted"))

            #makes a post object with commit=false to allow for editing
            #setting attributes
            post = form.save(commit=False)
            args = post.post_handler(community_wall[0], user)
            return HttpResponseRedirect('/user/home/')
        else: #if there is an error, asks user to fix it
            return HttpResponseRedirect('/user/home/')

    else:
        args.update(csrf(request))
        args['form'] = post_form(request.POST)
            #get ourUser from the request
        user = ourUser.objects.get(username=request.user.username)
        order_by = request.GET.get('order_by')
        if order_by:
            community_tools = Tool.objects.filter(community=user.community).filter(is_active=True).order_by(order_by)[:5]
        else:
            community_tools = Tool.objects.filter(community=user.community).filter(is_active=True)[:5]
        has_tools = bool(community_tools)
        args['user'] = user
        args['tools'] = community_tools
        args['has_tools'] = has_tools
        community = user.community
        args['comm'] = community
        #get posts
        user_community = user.community
        community_wall = communityWall.objects.filter(community=user_community).exclude(wall_name="deleted")
        args['posts'] = Post.objects.filter(wall=community_wall).order_by('-timestamp_post')
        return render(request,'home.html',args)

@loggedin
def community_users(request):
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    args['user'] = user
    order_by = request.GET.get('order_by')
    if order_by:
        all_users = ourUser.objects.filter(community=user.community,is_active=True).exclude(id=user.id).order_by(order_by)
    else:
        all_users = ourUser.objects.filter(community=user.community,is_active=True).exclude(id=user.id)
    args['all_users'] = all_users
    if user == user.community.admin:
        args['admin'] = 1 
    return render_to_response('community_members.html', args, context_instance=RequestContext(request))

@loggedin
def my_user(request):
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    args['user'] = user
    feed = FeedBack.objects.filter(user=user)
    args['tools'] = Tool.objects.filter(owner=args['user'])
    args['reputation'] = args['user'].reputation()
    args['feed'] = feed
    return render_to_response('user.html', args)


@loggedin
def show_user(request, user_id):
    args = {}
    args['this_user'] = ourUser.objects.get(id=user_id)
    args['user'] = get_object_or_404(ourUser,id=request.user.id)
    args['tools'] = Tool.objects.filter(owner=args['this_user'])
    args['reputation'] = args['this_user'].reputation()
    return render_to_response('users.html', args)

class update_user(UpdateView):
    model = ourUser
    form_class =  user_update_form
    template_name = 'update_user.html'
    success_url = '/user/home'

    def get_success_url(self):
        messages.success(self.request, "You have successfully updated your information")
        return self.success_url

    def get_object(self):
        return get_object_or_404(ourUser, id=self.request.user.id)
    
    def get(self,request,*args,**kwargs):
        user = get_object_or_404(ourUser, id=self.request.user.id)
        self.kwargs.update(csrf(self.request))
        self.kwargs['form'] = user_update_form()
        self.kwargs['user'] = user
        return render_to_response('update_user.html', self.kwargs)

@loggedin
def feedBack(request, reservation_id,mess_id):
    reservation = get_object_or_404(Reservation,id=reservation_id)
    user = get_object_or_404(ourUser,id=request.user.id)
    args = {}
    if request.POST:
        form = feed_back_form(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.post(reservation,mess_id)
            messages.success(request, "You have successfully posted feedback on " + reservation.borrower.username)
            return HttpResponseRedirect('/user/home/',args)
        else:
            args.update(csrf(request))
            args['form'] = form
            args['user'] = user
            args['error'] = 1
            return render_to_response('feed_back.html', args)
    else:
        if user == reservation.owner:
            form = feed_back_form()
            args['form'] = form
            if reservation.feed_back_given:
                args.update(csrf(request))
                args['user'] = user
                args['allReady'] = 1
                return render_to_response('feed_back.html', args)
            else:
                args.update(csrf(request))
                args['user'] = user
                return render_to_response('feed_back.html', args)
        else:
            args['user'] = user
            return render_to_response('401.html',args)

@loggedin
def lay_down_the_law(request,user_id):
    this_user = get_object_or_404(ourUser, id=user_id)
    user = get_object_or_404(ourUser,id=request.user.id)
    if user.community.admin != user:
        #you sir are an asshole
        args['user'] = user
        return render_to_response('401.html',args)
    elif this_user == user:
        #uncomment this line if your a baller
        #user.BANHAMMER()
        return HttpResponseRedirect('/user/logout')
    else:
        this_user.BANHAMMER()
        return HttpResponseRedirect('/user/users/')

@loggedin
def change_password_view(request):
    args = {}
    user = get_object_or_404(ourUser,id=request.user.id)
    args['user'] = user
    if request.POST:
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully changed your password")
            return HttpResponseRedirect('/user/home')
        else:
            args.update(csrf(request))

            args['form'] = form
            args['error'] = 1

            return render_to_response('change_password.html', args)
    else:
        form = password_change_form(user=request.user)

        args.update(csrf(request))

        args['form'] = form

        return render_to_response('change_password.html', args)
