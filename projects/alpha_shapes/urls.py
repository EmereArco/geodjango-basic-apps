from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import databrowse

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('clustr.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^databrowse/(.*)', databrowse.site.root),
)
    

urlpatterns += patterns('',
        (r'^media/(.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
    )