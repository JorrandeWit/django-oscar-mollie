from django.conf.urls import include, url
from django.contrib import admin

from oscar.app import application


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mollie/', include('mollie_oscar.urls', namespace='mollie_oscar')),
    url(r'^', include(application.urls)),
]
