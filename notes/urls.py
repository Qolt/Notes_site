from django.conf.urls import patterns, include, url
from notes_application.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^$', show_start_page),
    (r'^openid/', include('django_openid_auth.urls')),
    # Examples:
    # url(r'^$', 'notes.views.home', name='home'),
    # url(r'^notes/', include('notes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
