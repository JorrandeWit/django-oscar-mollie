![Mollie](https://www.mollie.nl/files/Mollie-Logo-Style-Small.png) 
![Oscar](https://github.com/django-oscar/django-oscar/raw/master/docs/images/logos/oscar.png)

# Mollie API client for Django Oscar #

Payment gateway integration between [Mollie API client](https://github.com/mollie/mollie-api-python) and [Django Oscar](https://github.com/django-oscar/django-oscar).

## Requirements ##
To use the Mollie API client, the following things are required:

+ Get yourself a free [Mollie account](https://www.mollie.nl/aanmelden). No sign up costs.
+ Create a new [Website profile](https://www.mollie.nl/beheer/account/profielen/) to generate API keys and setup your webhook.
+ Now you're ready to use the Mollie API client in test mode.
+ In order to accept payments in live mode, payment methods must be activated in your account. Follow [a few steps](https://www.mollie.nl/beheer/diensten), and let us handle the rest.
+ Mollie API client for Python has a dependency on [Requests](http://python-requests.org).

## Installation ##

You will need to set your [Mollie API Key](https://www.mollie.nl/beheer/account/profielen/) to connect to Mollie.

```
# settings.py
MOLLIE_API_KEY = 'secret-key-123'
```

Also, you need to define a mapping from the four possible [Mollie responses](https://www.mollie.com/nl/docs/reference/payments/get#example) to your [Oscar order statuses](http://django-oscar.readthedocs.io/en/releases-1.1/ref/settings.html#oscar-order-status-pipeline).
```
# settings.py
MOLLIE_STATUS_MAPPING = {
    'Paid': 'Being processed',
    'Pending': 'Pending Payment',
    'Open': 'Pending Payment',
    'Cancelled': 'Cancelled'
}
```

You need to make sure your webhook URI is accessible. To do so, include the following into your root URLs conf (you are free to whatever regex you may like):
```
url(r'^mollie/', include('mollie_oscar.urls', namespace='mollie_oscar')),
```

## Examples ##

Please visit the [sandbox](https://github.com/JorrandeWit/django-oscar-mollie/tree/master/sandbox) to see how to integrate Mollie into your Oscar application.

## Under Construction ##
The following will need to be added to this application.
+ Support Refunding payments
