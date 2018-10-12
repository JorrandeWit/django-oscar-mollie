from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import NoReverseMatch, reverse
from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .facade import Facade

from oscar.core.loading import get_class, get_model

OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
SourceType = get_model('payment', 'SourceType')
Source = get_model('payment', 'Source')


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(OrderPlacementMixin, View):
    """
    Handle a Mollie payment status change.
    """

    def get_message_context(self, order):
        """
        Make sure the mail context contains the User who originally ordered, not the current
        (anonymous) User.
        """
        ctx = super().get_message_context(order)
        ctx['user'] = ctx['order'].user

        if not ctx['user']:
            # Attempt to add the anon order status URL to the email template
            # ctx.
            try:
                path = reverse('customer:anon-order',
                               kwargs={'order_number': order.number,
                                       'hash': order.verification_hash()})
            except NoReverseMatch:
                # We don't care that much if we can't resolve the URL
                pass
            else:
                site = Site.objects.get_current()
                protocol = 'https' if settings.OSCAR_MOLLIE_HTTPS else 'http'
                ctx['status_url'] = '%s://%s%s' % (protocol, site.domain, path)
        else:
            ctx['status_url'] = None
        return ctx

    def post(self, request):
        with transaction.atomic():
            payment_id = request.POST.get('id')
            facade = Facade()
            facade.update_payment_status(payment_id)

            # Send Message now since this was blocked before
            order = facade.get_order(payment_id)

            # Only send confirmation if order is paid
            if order.status in settings.OSCAR_MOLLIE_CONFIRMED_STATUSES:
                self.send_confirmation_message(
                    order,
                    self.communication_type_code,
                )

        return HttpResponse(status=200)
