from django.conf.urls.defaults import *
from django.conf import settings
import os
from django.contrib import admin
admin.autodiscover()

import cropper

urlpatterns = patterns('',
    # Example:
    # (r'^demo_project/', include('demo_project.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^static/cropper-assets/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(
            os.path.realpath(os.path.dirname(cropper.__file__)), 'assets'
        )
    }),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.OUR_ROOT, 'static'),
    }),
    (r'^admin/(.*)', admin.site.root),
)
