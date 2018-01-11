from settings import *


ORDER_STATUS_PAID = 'Being processed'

# Oscar Shop settings
OSCAR_INITIAL_ORDER_STATUS = OSCAR_INITIAL_LINE_STATUS = 'Pending Payment'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending Payment': (ORDER_STATUS_PAID, 'Cancelled',),
    ORDER_STATUS_PAID: (ORDER_STATUS_PAID, 'Cancelled',),
    'Cancelled': (),
}
OSCAR_MOLLIE_CONFIRMED_STATUSES = [ORDER_STATUS_PAID]

# Mollie settings
MOLLIE_API_KEY = 'secret-key-123'
MOLLIE_STATUS_MAPPING = {
    'Paid': ORDER_STATUS_PAID,
    'Pending': 'Pending Payment',
    'Open': 'Pending Payment',
    'Cancelled': 'Cancelled'
}
