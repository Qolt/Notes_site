from django.conf.urls import patterns, include, url
from notes_application.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^$', 'notes.notes_application.views.show_start_page', name = "main"),
    url('^login/$', 'notes.notes_application.views.show_login_page', name = "login"),
    url('^logout/$', 'notes.notes_application.views.logout', name = "logout"),
    url(r'', include('social_auth.urls')),
    url('^create_note/$', 'notes.notes_application.views.create_note', name = "create_note"),
    url('^notes_list/$', 'notes.notes_application.views.notes_list', name = "notes_list"),
    # Examples:
    # url(r'^$', 'notes.views.home', name='home'),
    # url(r'^notes/', include('notes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
