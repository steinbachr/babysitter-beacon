from django.conf.urls import patterns, include, url
from django.contrib import admin
from web import urls as web_urls
from api import urls as api_urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urls)),
    url(r'', include(web_urls)),
)
