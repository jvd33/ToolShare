from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from django.contrib import admin
from userManagement import views
from userManagement.views import  update_user

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ToolShare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^register/', 'userManagement.views.register'),
    url(r'^login/$', 'userManagement.views.login_view'),
    url(r'^home/$', 'userManagement.views.home_view'),
    url(r'^logout/$', 'userManagement.views.logout_view'),
    url(r'^users/$', 'userManagement.views.community_users'),
    url(r'^myuser/$','userManagement.views.my_user'),
    url(r'^view/(?P<user_id>\d+)/$', 'userManagement.views.show_user'),
    url(r'^update/$', update_user.as_view(), name = 'update'),
    url(r'^changepassword/', 'userManagement.views.change_password_view'),
    url(r'^feedBack/(?P<reservation_id>\d+)/(?P<mess_id>\d+)/$', 'userManagement.views.feedBack'),
    url(r'^banUser/(?P<user_id>\d+)/$', 'userManagement.views.lay_down_the_law'),
)
