from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nes_phone/', include('nes_phone.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    
    (r'^nes/.*/media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
                       
    (r'^nes/phoneroam/$', 'phone_roam.views.home'),
    (r'^nes/phoneroam/subscription/$','phone_roam.views.xhr_subscription'),
    (r'^nes/handle/$', 'nes_api_rest.views.handle'),
    
    (r'^nes/polite/$', 'polite_busy.views.show_messages'),
    (r'^nes/polite/messages/$', 'polite_busy.views.control_messages'),
)
