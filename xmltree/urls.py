from django.conf.urls import patterns, include, url
from maker_xml.views import create_xml
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xmltree.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^xmltree/', include('maker_xml.urls')),
	
                       
)
