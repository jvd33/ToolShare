from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from messageBoard.forms import communityWall_form, post_form
from messageBoard.models import communityWall, Post
from userManagement.models import ourUser
from ToolShare.decorators import loggedin


#makes a community_wall
@loggedin
def create_community_wall(request):
    args = {}
    args['user'] = get_object_or_404(ourUser, id=request.user.id)
    if request.POST:
        form = communityWall_form(request.POST)
        if form.is_valid():
            form.save()
            #save it and complete
            return HttpResponseRedirect('/messageBoard/index')
        else:
            form = communityWall_form()
            args.update(csrf(request))
            #when there is a problem, error
            args['form'] = form
            args['error'] = 1
            return render_to_response('create_community_wall.html', args)
    else: #user needs to fill out form
        form = communityWall_form()
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('create_community_wall.html', args)

#displays all the posts in a listing
@loggedin
def display_posts(request):

    #fetches our user object, sets the params to return in the template
    user = get_object_or_404(ourUser,id=request.user.id)

    user_community = user.community
    community_wall = communityWall.objects.filter(community=user_community).exclude(wall_name="deleted")

    #returns all post objects for the wall, most recent first
    return render_to_response('posts.html',{
        'posts':Post.objects.filter(wall=community_wall).order_by('-timestamp_post'),'user':user
        })

#returns a post when called for
@loggedin
def post(request, post_id=1):
    args = {}
    args['post'] = get_object_or_404(Post, id=post_id)

    poster = args['post'].poster
    user = get_object_or_404(ourUser,id=request.user.id)

    args['user'] = user
    args['poster'] = poster
    return render_to_response('post.html', args)

#makes a post to the wall
@loggedin
def add_post(request):
    args = {}
    args['user'] = get_object_or_404(ourUser,id=request.user.id)
    form = post_form()
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
            args = {}
            args.update(csrf(request))
            args['form'] = form
            args['error'] = 1
            return render_to_response('add_post.html', args)
    else:
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('add_post.html', args)
@loggedin
def delete_post(request, post_id=1):
    user = get_object_or_404(ourUser,id=user.request.id)
    post = get_object_or_404(Post, id=post_id)
    if post.poster == user:
        post.delete()
        return HttpResponseRedirect('/user/home/')
    else:
        args['user'] = user
        return render_to_response('401.html',args)


