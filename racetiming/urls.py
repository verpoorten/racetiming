
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from timing.views import common
from django.contrib.auth import views as auth_views


urlpatterns = (
    # url(r'^login/$', common.login, name='login'),
    # url(r'^logout/$', common.log_out, name='logout'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'', include('timing.urls')),
    url(r'', include('website.urls'))
)
