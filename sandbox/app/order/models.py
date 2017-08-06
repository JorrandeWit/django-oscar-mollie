from django.conf import settings

from oscar.apps.order.abstract_models import AbstractOrder


class Order(AbstractOrder):
    def is_open_payment(self):
        return self.status == settings.ORDER_PENDING_STATUS

    def is_cancelled_order(self):
        return self.status == settings.ORDER_CANCELLED_STATUS


from oscar.apps.order.models import *
