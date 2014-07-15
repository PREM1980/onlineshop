from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from onlineapp.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test',TemplateView.as_view(template_name='testpage.html')),
    url(r'^$',loginpage),
    url(r'^googleauthlogin',googleauthlogin),
    url(r'^mainpage',mainpage),
    url(r'^createpdf',createpdf),
    url(r'^createexcel',createexcel),
    url(r'^createdoc',createdoc),
    url(r'^startpage',startpage),
    url(r'^getproductinfo',getproductinfo),
    url(r'^category/(?P<categoryid>[^/]+)/$',categorypage, name='category-page'),
    #url(r'^articles/(?P<year>        )/$', 'news.views.year_archive'),
    url(r'',include('social_auth.urls')),
    #url(r'^login/$',redirect_to,{'url':'/login/google'}),
    #url(r'^login/$', RedirectView.as_view(url='/login/google'))

)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
