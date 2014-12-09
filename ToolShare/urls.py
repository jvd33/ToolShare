from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ToolShare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^user/', include('userManagement.urls', namespace="user")),
    url(r'^user/', include('userMessaging.urls')),

    url(r'^toolshare/', include('toolshareapp.urls')),
    url(r'^board/', include('messageBoard.urls')),

    url(r'^$', TemplateView.as_view(template_name="index.html")),

)
