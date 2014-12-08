from django.conf.urls import patterns, url


urlpatterns = patterns('web.views',
    url(r'^/?$', 'home'),
    url(r'^logout/?$', 'app_logout'),
    url(r'^parent-signup/?$', 'parent_signup'),
    url(r'^sitter-signup/?$', 'sitter_signup'),
    url(r'^parents/(?P<slug>[A-Za-z0-9\-]+)/?$', 'parents_dashboard'),
    url(r'^sitters/(?P<slug>[A-Za-z0-9\-]+)/?$', 'sitters_dashboard'),
)
