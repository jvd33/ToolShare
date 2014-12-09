from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^inbox/$', 'userMessaging.views.inbox'),
    url(r'^message/(?P<message_id>\d+)/$', 'userMessaging.views.view_message'),
    url(r'^newmessage/$', 'userMessaging.views.send_message'),
    url(r'^sentmessages/$', 'userMessaging.views.sent_messages'),
    url(r'^delete/(?P<message_id>\d+)/$', 'userMessaging.views.delete_message'),
)