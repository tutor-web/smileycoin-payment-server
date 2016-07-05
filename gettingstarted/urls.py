from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^generateAddress', hello.views.generateAddress, name='generateAddress'),
    url(r'^postTX', hello.views.postTX, name='postTX'),
    url(r'^getToken', hello.views.getToken, name='getToken'),
    url(r'^verifyPayment', hello.views.verifyPayment, name='verifyPayment'),
    url(r'^admin/', include(admin.site.urls)),
]
