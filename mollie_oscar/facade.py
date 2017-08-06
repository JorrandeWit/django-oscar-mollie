import logging
from decimal import Decimal

from django.contrib.sites.models import Site
from django.conf import settings
from django.http import Http404
from django.urls import reverse

import Mollie
from oscar.apps.payment.exceptions import UnableToTakePayment
from oscar.core.loading import get_model

logger = logging.getLogger('oscar.checkout')

Order = None
SourceType = None


def _lazy_get_payment_event_models():
    global PaymentEvent
    global PaymentEventType
    global PaymentEventQuantity

    PaymentEvent = get_model('order', 'PaymentEvent')
    PaymentEventType = get_model('order', 'PaymentEventType')
    PaymentEventQuantity = get_model('order', 'PaymentEventQuantity')


def _lazy_get_models():
    # Avoids various import conflicts between apps that may
    # import the Facade before any other models.
    global Order
    global Source
    global SourceType
    if not Order:
        Order = get_model('order', 'Order')
        Source = get_model('payment', 'Source')
        SourceType = get_model('payment', 'SourceType')


class Facade(object):
    def __init__(self):
        self.mollie = Mollie.API.Client()
        self.mollie.setApiKey(settings.MOLLIE_API_KEY)

    def create_payment(self, order_number, total, description=None, redirect_url=None):
        if not redirect_url:
            redirect_url = reverse('customer:order', kwargs={'order_number': order_number})

        site = Site.objects.get_current()
        redirect_url = 'http://%s%s' % (site.domain, redirect_url)

        payment = self.mollie.payments.create({
            'amount': float(total),
            'description': description or self.get_default_description(order_number),
            'redirectUrl': redirect_url,
            'webhookUrl':  self.get_webhook_url(),
            'metadata': {
                'order_nr': order_number
            }
        })

        return payment['id']

    def get_default_description(self, order_number):
        return 'Order {0}'.format(order_number)

    def get_payment_url(self, payment_id):
        """
        Return the customer's payment URL
        """
        payment = self.mollie.payments.get(payment_id)
        return payment.getPaymentUrl()

    def get_webhook_url(self):
        # TODO: Make this related to this app without explicit namespace declaration...?
        site = Site.objects.get_current()
        return 'http://%s%s' % (site.domain, reverse('mollie_oscar:webhook'))

    def get_order(self, payment_id, order_nr=None):
        _lazy_get_models()

        try:
            assert order_nr
            order = Order.objects.get(number=order_nr,
                                      sources__reference=payment_id,
                                      sources__source_type=self.get_source_type())
        except AssertionError:
            order = Order.objects.get(sources__reference=payment_id,
                                      sources__source_type=self.get_source_type())
        except Order.DoesNotExist:
            raise Http404(u"Order with transaction {0} not found".format(payment_id))

        return order

    def update_payment_status(self, payment_id):
        """
        The Mollie payment status has changed. Translate this status update to Oscar.
        """
        payment = self.mollie.payments.get(payment_id)
        amount = Decimal(payment.get('amount'))
        try:
            order_nr = payment.get['metadata']['order_nr']
        except TypeError:
            order_nr = None
        order = self.get_order(payment_id, order_nr)

        if payment.isPaid():
            status_code = 'Paid'
            self.complete_order(order, amount, payment_id, status_code)
        elif payment.isPending():
            status_code = 'Pending'
        elif payment.isOpen():
            status_code = 'Open'
        else:
            status_code = 'Cancelled'

        self.update_order_payment(order, status_code)
        self.register_payment_event(order, amount, payment_id)

    def complete_order(self, order, amount, reference, status_code):
        try:
            source = order.sources.get(source_type=self.get_source_type(), reference=reference)
            source.debit(amount, reference=reference, status=status_code)
        except Source.DoesNotExist:
            raise UnableToTakePayment('Shit men... What happened?')

    def update_order_payment(self, order, status_code):
        order.set_status(settings.MOLLIE_STATUS_MAPPING[status_code])

    def register_payment_event(self, order, amount, reference):
        _lazy_get_payment_event_models()
        event_type, __ = PaymentEventType.objects.get_or_create(name=order.status)

        event = PaymentEvent(event_type=event_type, amount=amount,
                             reference=reference, order=order)
        event.save()

        # We assume all lines are involved in the initial payment event
        for line in order.lines.all():
            PaymentEventQuantity.objects.create(event=event, line=line, quantity=line.quantity)

    def get_source_type(self):
        _lazy_get_models()
        source_type, __ = SourceType.objects.get_or_create(code='mollie',
                                                           defaults={'name': 'Mollie'})
        return source_type
