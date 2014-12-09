from django.shortcuts import render, render_to_response
from toolshareapp.models import Tool, Shed, Community, Reservation
from userMessaging.models import Message
from django.http import HttpResponse, HttpResponseRedirect
from toolshareapp.forms import *
from django.core.context_processors import csrf
from userManagement.models import ourUser, FeedBack
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import datetime
from django.template import RequestContext
from django.views.generic.edit import UpdateView
from ToolShare.decorators import loggedin
import time
from django.contrib import messages

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


"""
Tool views
"""
@loggedin
def register_tool(request):
    #if this is a post request
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    args['user'] = user
    if request.POST:
        temp_user = ourUser.objects.get(username=request.user.username)
        form = tool_form(temp_user, data=request.POST)
        if form.is_valid():
            tool = form.save(commit=False) #create but dont save the tool
            tool.create(user)

            #supposed to show success message
            messages.success(request,"You have successfully registered " + tool.name)
            return HttpResponseRedirect('/user/home')
        else:
            #if there are errors say there are
            args.update(csrf(request))
            args['form'] = form
            args['error'] = 1
            args['sheds']= Shed.objects.filter(community=user.community)
            return render_to_response('register_tool.html', args)
    else:

        #
        #if it is a get request just genrate the form
        user = get_object_or_404(ourUser, username=request.user.username)
        form = tool_form(user=user)
        args.update(csrf(request))
        args['form'] = form
        args['sheds']= Shed.objects.filter(community=user.community)
        return render_to_response('register_tool.html', args)
@loggedin
def display_tools(request):
    #view that displays tools (might not be used)
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    order_by = request.GET.get('order_by')
    if order_by:
        my_tools = Tool.objects.filter(owner=user).order_by(order_by)
    else:
        my_tools = Tool.objects.filter(owner=user)
    args['user'] = user
    args['tools'] = my_tools
    return render_to_response('my_tools.html',args, context_instance=RequestContext(request))

@loggedin
def display_requests(request):
    #view your current requests for tool borrowing
    user = get_object_or_404(ourUser, id=request.user.id)
    args = {}
    args['user'] = user
    reservations = Reservation.objects.filter(owner=user,approved=False)
    args['reservations'] = reservations
    if len(reservations) == 0:
        args['some'] = 1
    return render_to_response('borrow_requests.html',args)

@loggedin
def accept_request(request, res_id):
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    reservation = get_object_or_404(Reservation, id=res_id)
    if user == reservation.owner:
        reservation.approved = True
        reservation.send_accept()
        reservation.save()
        args['user'] = user
        args['status'] = "Tool reservation accepted."
        return render_to_response('reserve_tools.html', args, context_instance=RequestContext(request))
    else:
        args['user'] = user
        return render_to_response('401.html',args)

@loggedin
def deny_request(request, res_id):
    args = {}
    user = get_object_or_404(ourUser,id=request.user.id)
    reservation = get_object_or_404(Reservation, id=res_id)
    args['user'] = user
    if request.POST:
        reservation.send_deny(request.POST.get('content'))
        reservation.delete()
        args.update(csrf(request))
        args['status'] = "Tool reservation denied."
        return render_to_response('reserve_tools.html', args, context_instance=RequestContext(request))
    else:
        if user == reservation.owner:
            args.update(csrf(request))
            return render_to_response('deny_request.html',args)
        else:
            return render_to_response('401.html',args)

@loggedin
def borrowed_tools(request):
    user = get_object_or_404(ourUser, id=request.user.id)
    args = {}
    order_by = request.GET.get('order_by')
    if order_by:
        if "owner" in order_by:
            order_by += "__username"
        borrowed_tools = Tool.objects.filter(borrower=user).order_by(order_by)
    else:
        borrowed_tools = Tool.objects.filter(borrower=user)
    args['user'] = user
    args['tools'] = borrowed_tools
    return render_to_response('borrowed_tools.html',args, context_instance=RequestContext(request))

@loggedin
def community_tools(request):
    #get all tools in that community
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    order_by = request.GET.get('order_by')
    if order_by:
        if "owner" in order_by:
            order_by += "__username"
        community_tools = Tool.objects.filter(community=user.community).filter(is_active=True).order_by(order_by)
    else:
        community_tools = Tool.objects.filter(community=user.community).filter(is_active=True)
    has_tools = bool(community_tools)
    args['user'] = user
    args['tools'] = community_tools
    args['has_tools'] = has_tools
    return render_to_response('community_tools.html', args, context_instance=RequestContext(request))

@loggedin
def tool(request, Tool_id):
    #get a specific tool
    args = {}
    tool = get_object_or_404(Tool, id=Tool_id)
    reservations = Reservation.objects.filter(tool=tool,is_complete=False,skipped=False)
    args['tool'] = tool
    user = get_object_or_404(ourUser, id=request.user.id)
    args['address'] = tool.get_address(user)
    #the user who is on the page for use of an edit button
    curr_user = ourUser.objects.get(username=request.user.username)
    #check to see if the tool in in the default home shed
    args['user'] = user
    args['curr_user'] = curr_user
    args['is_admin'] = tool.is_admin(curr_user)
    args['reservations'] = reservations
    return render_to_response('tool.html',args)

@loggedin
def deactivate_tool(request, Tool_id):
    tool = get_object_or_404(Tool, id=Tool_id)
    res = Reservation.objects.filter(tool=tool,is_complete=False)
    if tool.remove(res):
        return HttpResponseRedirect('/toolshare/mytools/')
    else:
        args = {}
        user = get_object_or_404(ourUser,id=request.user.id)
        args['user'] = user
        res = list(res)
        args['borrower'] = res[0].borrower
        return render_to_response('currently_in_use.html',args)

@loggedin
def activate_tool(request, Tool_id):
    
    tool = get_object_or_404(Tool, id=Tool_id)
    tool.activate()
    return HttpResponseRedirect('/toolshare/mytools/')

class update_tool(UpdateView):
    #must be given the tool id in a url variable named pk THIS IS VERY IMPORTANT
    model = Tool  #specify the model it is using
    form_class = tool_form  #specify the form that it is using
    template_name = 'update_tool.html'  #give it a template
    success_url = '/toolshare/communitytools'  #were should it go if the update is success

    def get_success_url(self):
        messages.success(self.request, "You have successfully updated the tool")
        return self.success_url

    def get(self,request,*args,**kwargs):
        #args={}
        user = get_object_or_404(ourUser,id=self.request.user.id)
        sheds = Shed.objects.filter(community=user.community).exclude(id=self.get_object().shed.id)
        self.kwargs.update(csrf(self.request))
        self.kwargs['tool'] = self.get_object
        self.kwargs['sheds'] = sheds
        self.kwargs['user'] = user
        #args['notify'] = ("you have successfully updated your tool")
        #works for update shed and update community, not for tool
        return render(request,'update_tool.html', self.kwargs)

@loggedin
def remove_tool_from_shed(request, tool):
    #an admin of a shed removes a tool from a shed 
    tool = Tool.objects.get(id=tool)
    #that tool is sent back to the users house
    shed = Shed.objects.get(name="Home",community=tool.community)
    tool.shed = shed
    tool.save()
    return HttpResponseRedirect('/toolshare/viewsheds')

"""
Shed views
"""
#see tool for documentation
@loggedin
def register_shed(request):
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    args['user'] = user
    if request.POST:
        form = shed_form(request.POST)
        if form.is_valid():
            shed = form.save(commit=False)
            admin = get_object_or_404(ourUser, id=request.user.id)
            shed.create(admin)
            messages.success(request, "You have successfully created a shed called " + shed.name)
            return HttpResponseRedirect('/user/home')
        else:
            args.update(csrf(request))
            args['form'] = form
            args['error'] = 1
            return render_to_response('register_shed.html', args)
    else:
        form = shed_form()
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('register_shed.html', args)

#allows the user to see sheds
@loggedin
def view_sheds(request):
    user = get_object_or_404(ourUser, id=request.user.id)
    sheds = Shed.objects.filter(admin=user)
    if user.community.admin == user:
        sheds = Shed.objects.filter(community=user.community).exclude(is_home=True)
    args = {}
    args['sheds'] = sheds
    args['user'] = user
    return render_to_response('view_sheds.html',args, context_instance = RequestContext(request))

#the view shed function to view a shed's information
@loggedin
def view_shed(request, shed=1):
    args = {}
    shed = get_object_or_404(Shed, id=shed)
    user = get_object_or_404(ourUser,id=request.user.id)
    args['shed'] = shed
    args['tools'] = Tool.objects.filter(shed = shed.id)
    args['user'] = user
    if shed.admin == user:
        args['admin'] = 1
    return render_to_response('shed.html',args)


#class to allow a shed to be edited
class update_shed(UpdateView):
    model = Shed
    form_class = shed_form
    template_name = 'update_shed.html'
    success_url = '/user/home'
    #if success_url:
        #messages.success("you have successfully updated" )

    def get_success_url(self):
        messages.success(self.request, "You have successfully updated the shed")
        return self.success_url
    
    def get(self,request,*args,**kwargs):
        user = get_object_or_404(ourUser,id=self.request.user.id)
        self.kwargs.update(csrf(self.request))
        self.kwargs['user'] = user
        self.kwargs['shed'] = self.get_object
        return render_to_response('update_shed.html', self.kwargs)

"""
Reservation views
"""
#reserve tool R2, not called at all by R1
@loggedin
def reserve_tool(request, tool):
    args = {}
    tool = get_object_or_404(Tool, id=tool)
    borrower = get_object_or_404(ourUser, id=request.user.id)
    owner = get_object_or_404(ourUser, id=tool.owner.id)
    community = get_object_or_404(Community,id=tool.community.id)
    reservations = Reservation.objects.filter(tool=tool,is_complete=False,skipped=False)
    args['user'] = borrower
    args['tool'] = tool
    args['reservations'] = reservations
    if request.POST:
        form = reservation_form(request.POST)
        args['form'] = form
        if form.is_valid():
            #get all the reservations forr that tool that are not complete or skipped
            this_tools_reservations = list(Reservation.objects.filter(tool=tool.id).filter(is_complete=False).filter(skipped=False))
            for res in this_tools_reservations:
                #check to see if the request date falls within the reqeuest and return date of another tool
                if form.cleaned_data['borrow_request_date'] <= res.return_date and form.cleaned_data['borrow_request_date'] >= res.borrow_request_date:      
                    args['error'] = 5
                    return render_to_response('reserve_tools.html', args, context_instance=RequestContext(request))
                #check to see if the return data is within another revervations request and return date
                if form.cleaned_data['return_date'] >= res.borrow_request_date and form.cleaned_data['return_date'] <= res.return_date:
                    args['error'] = 5
                    return render_to_response('reserve_tools.html', args, context_instance=RequestContext(request))
                #check to see if the request date is before another request date and the return date is after another return date
                if form.cleaned_data['borrow_request_date'] <= res.borrow_request_date and form.cleaned_data['return_date'] >= res.return_date:
                    args['error'] = 5
                    return render_to_response('reserve_tools.html', args, context_instance=RequestContext(request))
            #if the return date is before the request date
            if form.cleaned_data['return_date'] <= form.cleaned_data['borrow_request_date']:
                args['error'] = 4
                return render_to_response('reserve_tools.html', args, context_instance=RequestContext(request))
            #If nothing is wrong make the reservation
            reservation = form.save(commit=False)
            tool.reserve(reservation, borrower)
            args['tool'] = tool
            args['status'] = "Tool requested."
            messages.success(request, "You have successfully set the reservation")
            return render_to_response('tool.html', args , context_instance=RequestContext(request))
        #form is not valid
        else:
            args.update(csrf(request))
            args['error'] = 1
            return render_to_response('reserve_tools.html', args, context_instance=RequestContext(request))
    #it is not a post request
    else:
        form = reservation_form()
        args.update(csrf(request))
        args['tool'] = tool
        args['form'] = form
        return render_to_response('reserve_tools.html', args, context_instance=RequestContext(request))

@loggedin
def return_tool(request, tool):
    args = {}
    tool = get_object_or_404(Tool, id=tool)
    borrower = get_object_or_404(ourUser, id=tool.borrower.id)
    user = get_object_or_404(ourUser,id=request.user.id)
    args['user'] = user
    if request.user.id == borrower.id:
        if tool.shed.is_home:
            tool.return_from_home(False)
        else:
            tool.return_tool()
        messages.success(request, "you have returned " + tool.name)
        return render_to_response('borrowed_tools.html', args, context_instance=RequestContext(request))
    else:
        status = "You are not the current holder of this tool"
        args['status'] = status
        return render_to_response('borrowed_tools.html', args)

@loggedin
def approve_return(request,res_id,mess_id):
    user = get_object_or_404(ourUser,id=request.user.id)
    reservation = get_object_or_404(Reservation,id=res_id)
    if user == reservation.owner:
        tool = reservation.tool
        tool.return_from_home(True,mess_id)
        return HttpResponseRedirect('/user/inbox/')
    else:
        args = {}
        args['user'] = user
        return render_to_response('401.html',args)

"""
Community Views
"""
@loggedin
def chose_community(request):
    args = {}
    user = get_object_or_404(ourUser,id=request.user.id)
    args['user'] = user
    coms = Community.objects.filter(is_active=True)
    args['coms'] = coms

    return render_to_response('chose_community.html',args)

@loggedin
def chose_communityft(request):
    args = {}
    user = get_object_or_404(ourUser,id=request.user.id)
    args['user'] = user
    coms = Community.objects.filter(is_active=True)
    args['coms'] = coms
    return render_to_response('chose_community_ft.html',args)

@loggedin
def select(request, community_id):
    user = get_object_or_404(ourUser, id=request.user.id)
    community = get_object_or_404(Community, pk=community_id)
    tools = list(Tool.objects.filter(owner=user))
    reserved = list(Tool.objects.filter(borrower=user))
    lent = list(Reservation.objects.filter(owner=user, skipped=False, is_active=True))
    reservation = list(Reservation.objects.filter(borrower=user, skipped=False, is_active=True))
    user.switch_comm_admin()
    time.sleep(1)
    user.switch_shed_admin()
    time.sleep(1)
    user.join(community, tools, lent, reserved, reservation)
    return HttpResponseRedirect('/user/home')

@loggedin
def new_community(request):
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    args['user'] = user
    if request.POST:
        form = community_form(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.make_community(user)
            return HttpResponseRedirect('/user/home')
        else:
            args.update(csrf(request))
            args['form'] = form
            args['error'] = 1
            return render_to_response('create_community.html', args)
    else:
        form = community_form()
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('create_community.html', args)

@loggedin
def new_admin(request):
    args = {}
    user = get_object_or_404(ourUser, id=request.user.id)
    args['user'] = user
    users = ourUser.objects.filter(community=user.community).exclude(id=user.id)
    args['users'] = users
    return render_to_response('some_page.html',args)

#allows user to update the community information if sufficient permissions
class update_community(UpdateView):
    model = Community
    form_class = community_form
    template_name = 'update_community.html'
    success_url = '/user/home'

    #this method is the only way i could send a message to all users
    #gets called when the UpdateView is called and submitted
    def get_success_url(self):
        #self.object is the community being edited
        community = self.object
        #gets every user in the community
        community_members = list(ourUser.objects.filter(community=community))
        admin = community.admin
        #for every user in the community, create and send a message
        for user in community_members:
            community.chain_mail(admin, user)
        #return the success url as usual
        messages.success(self.request, "You have successfully updated the community")
        return self.success_url

    def get(self,request,*args,**kwargs):
        user = get_object_or_404(ourUser,id=self.request.user.id)
        self.kwargs.update(csrf(self.request))
        self.kwargs['community'] = self.get_object
        self.kwargs['user'] = user
        return render_to_response('update_community.html', self.kwargs)

@loggedin
def stats(request):
    user = get_object_or_404(ourUser, id=request.user.id)
    community = user.community
    #initialize a stat object
    stat = Statistics(community)
    #generate the stats for a community
    data = stat.generate()
    #pop the flags off of the dict returned in generate()
    flags = data.pop('flags')
    args = {}
    #pass the view the data and flags list to the template
    args['data'] = data
    args['flags'] = flags
    args['user'] = user
    return render_to_response('stats.html', args)

#request holds the search string
#returns all objects with the search string somewhere in their name.
@loggedin
def search_objects(request): #the request holds the string query
    user = get_object_or_404(ourUser, id=request.user.id)
    string = request.GET['q']
    tools = Tool.objects.filter(community=user.community)
    users = ourUser.objects.filter(community=user.community)
    tool_results = []
    user_results = []
    for tool in tools:
        if string.lower() in tool.name.lower():
            tool_results.append(tool)
    for u in users:
        if string.lower() in u.username.lower():
            user_results.append(u)
    args = {}
    args['q'] = string
    args['tools'] = tool_results
    args['users'] = user_results
    args['user'] = user
    return render_to_response('results.html', args)

