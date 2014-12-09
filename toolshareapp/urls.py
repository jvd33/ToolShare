from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from django.contrib import admin
from toolshareapp import views
from toolshareapp.views import update_tool,update_shed,update_community

urlpatterns = patterns('',
    url(r'^registertool/$','toolshareapp.views.register_tool'),
    url(r'^registershed/$','toolshareapp.views.register_shed'),
    url(r'^viewsheds/$','toolshareapp.views.view_sheds'),
    url(r'^mytools/$', 'toolshareapp.views.display_tools'),
    url(r'^borrowrequests/$', 'toolshareapp.views.display_requests'),
    url(r'^acceptrequest/(?P<res_id>\d+)/$', 'toolshareapp.views.accept_request'),
    url(r'^denyrequest/(?P<res_id>\d+)/$', 'toolshareapp.views.deny_request'),
    url(r'^borrowedtools/$', 'toolshareapp.views.borrowed_tools'),
    url(r'^view/(?P<Tool_id>\d+)/$', 'toolshareapp.views.tool'),
    url(r'^viewshed/(?P<shed>\d+)/$', 'toolshareapp.views.view_shed'),
    url(r'^communitytools/', 'toolshareapp.views.community_tools'),
    url(r'^reservetools/(?P<tool>\d+)/$', 'toolshareapp.views.reserve_tool'),
    url(r'^returntool/(?P<tool>\d+)/$', 'toolshareapp.views.return_tool'),
    url(r'^updatetool/(?P<pk>\d+)/$', update_tool.as_view(), name = 'updatetool'),
    url(r'^updateshed/(?P<pk>\d+)/$', update_shed.as_view(), name = 'updateshed'),
    url(r'^updatecommunity/(?P<pk>\d+)/$', update_community.as_view(), name = 'updatecommunity'),
    url(r'^removefromshed/(?P<tool>\d+)/$', 'toolshareapp.views.remove_tool_from_shed'),
    url(r'^statistics/$', 'toolshareapp.views.stats'),
    url(r'^select/$', 'toolshareapp.views.chose_communityft'),
    url(r'^select/(?P<community_id>\d+)$', 'toolshareapp.views.select'),
    url(r'^newCommunity/$', 'toolshareapp.views.new_community'),
    url(r'^activate/(?P<Tool_id>\d+)/$', 'toolshareapp.views.activate_tool'),
    url(r'^deactivate/(?P<Tool_id>\d+)/$', 'toolshareapp.views.deactivate_tool'),
    url(r'^change_community/$', 'toolshareapp.views.chose_community'),
    url(r'^approveReturn/(?P<res_id>\d+)/((?P<mess_id>\d+))/$', 'toolshareapp.views.approve_return'),
    url(r'^results/$', 'toolshareapp.views.search_objects'),

)
