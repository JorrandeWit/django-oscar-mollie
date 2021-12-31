from django.conf.urls import url

from . import views


app_name = "mollie_oscar"

urlpatterns = [
    url(r'^webhook/', views.WebhookView.as_view(), name='webhook'),
]
