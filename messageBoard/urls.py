from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from django.contrib import admin
from messageBoard import views


admin.autodiscover()

#urls here

urlpatterns = patterns('',
    url(r'^create_community_wall/$','messageBoard.views.create_community_wall'),
	url(r'^posts/$', 'messageBoard.views.display_posts'),
    #passes in the post id as a variable for the url
	url(r'^view/(?P<post_id>\d+)/$', 'messageBoard.views.post'),
    url(r'^addpost/$', 'messageBoard.views.add_post'),
    url(r'^delete/(?P<post_id>\d+)/$', 'messageBoard.views.delete_post'),
)

