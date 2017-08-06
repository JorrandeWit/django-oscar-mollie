from settings import *


# Oscar Shop settings
OSCAR_INITIAL_ORDER_STATUS = OSCAR_INITIAL_LINE_STATUS = 'Pending Payment'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending Payment': ('Being processed', 'Cancelled',),
    'Being processed': ('Being processed', 'Cancelled',),
    'Cancelled': (),
}

# Mollie settings
MOLLIE_API_KEY = 'secret-key-123'
MOLLIE_STATUS_MAPPING = {
    'Paid': 'Being processed',
    'Pending': 'Pending Payment',
    'Open': 'Pending Payment',
    'Cancelled': 'Cancelled'
}
