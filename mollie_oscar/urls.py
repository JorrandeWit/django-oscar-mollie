from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^webhook/', views.WebhookView.as_view(), name='webhook'),
]
