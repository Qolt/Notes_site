from django.conf.urls import patterns, include, url
from notes_application import views 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^$', views.show_start_page, name = "main"),
    url('^login/$', views.show_login_page, name = "login"),
    url('^logout/$', views.logout, name = "logout"),
    url(r'', include('social_auth.urls')),
    url('^notes_list/$', views.notes_list, name = "notes_list"),
    url('^add_email/$', views.add_email, name = "add_email"),
    url('^check_email/$', views.check_email, name = "check_email"),
    url('^confirm/([A-Za-z0-9]{,33})$', views.confirm_email, name = "confirm"),

    url('^notes_lists/$', views.notes_lists, name = "notes_lists"),

    url('^note_content/([0-9]+)/ajax$', views.note_content, name = "note_content"),
    url('^note_content/$', views.note_content, name = "note_content"),
    url('^note_content/([0-9]+)$', views.notes_list, name = "note_content"),

    url('^delete_note/([0-9]+)$', views.delete_note, name = "delete_note"),
    url('^delete_note/$', views.delete_note, name = "delete_note"),

    url('^save_note/$', views.save_note, name = "save_note"),
    url('^save_note/([0-9]+)$', views.save_note, name = "save_note"),

    url('^edit_note/([0-9]+)$', views.edit_note, name = "edit_note"),
    url('^edit_note/$', views.edit_note, name = "edit_note"),

    url('^notes_menu/([0-9]+)$', views.notes_menu, name = "notes_menu"),
    url('^notes_menu/$', views.notes_menu, name = "notes_menu"),

    url('^notes_menu/(?P<sort>date|importance|shared)$', views.notes_menu, name = "notes_menu"),
    # Examples:
    # url(r'^$', 'notes.views.home', name='home'),
    # url(r'^notes/', include('notes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
