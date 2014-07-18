from django.conf.urls import patterns, include, url
from maker_xml.views import create_xml, MyRegistrationView
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xmltree.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^xmltree/', include('maker_xml.urls')),

    url(r'^/password/change/$',
                    auth_views.password_change,
                    name='password_change'),
    url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$',
                    auth_views.password_reset, {'template_name' : 'registration/password_reset_form_custom.html'},
                    name='password_reset'),
                       
    url(r'^accounts/password/reset/done/$',
                    auth_views.password_reset_done, {'template_name' : 'registration/password_reset_done_custom.html'},
                    name='password_reset_done'),
    
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                            auth_views.password_reset_confirm, {'template_name' : 'registration/password_reset_confirm_custom.html'},
                            name='password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$',auth_views.password_reset_complete,{'template_name' : 'registration/password_reset_complete_custom.html'},
                    name='password_reset_complete'),
    
   
    url(r'^accounts/profile/$', 'maker_xml.views.account_profile'),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

	
                       
)
