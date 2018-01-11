![Mollie](https://www.mollie.nl/files/Mollie-Logo-Style-Small.png)
![Oscar](https://github.com/django-oscar/django-oscar/raw/master/docs/images/logos/oscar.png)

# Mollie API client for Django Oscar #

Payment gateway integration between [Mollie API client](https://github.com/mollie/mollie-api-python) and [Django Oscar](https://github.com/django-oscar/django-oscar).

[![PyPI version](https://badge.fury.io/py/django-oscar-mollie.svg)](https://badge.fury.io/py/django-oscar-mollie)

## Installation ##

The easiest way to install is with [pip](https://pip.pypa.io).
```
$ pip install django-oscar-mollie
```


## Getting Started ##
You need to set your [Mollie API Key](https://www.mollie.nl/beheer/account/profielen/) to connect to Mollie.
```python
# settings.py
MOLLIE_API_KEY = 'secret-key-123'
```

Also, you need to define a mapping from the four possible [Mollie responses](https://www.mollie.com/nl/docs/reference/payments/get#example) to your [Oscar order statuses](http://django-oscar.readthedocs.io/en/releases-1.1/ref/settings.html#oscar-order-status-pipeline).
```python
# settings.py
MOLLIE_STATUS_MAPPING = {
    'Paid': ORDER_STATUS_PAID,
    'Pending': 'Pending Payment',
    'Open': 'Pending Payment',
    'Cancelled': 'Cancelled'
}
```

You need to make sure your webhook URI is accessible. To do so, include the following into your root URLs conf (you are free to choose whatever regex you may like):
```python
url(r'^mollie/', include('mollie_oscar.urls', namespace='mollie_oscar')),
```

## Examples ##

Please visit the [sandbox](https://github.com/JorrandeWit/django-oscar-mollie/tree/master/sandbox) to see how to integrate Mollie into your Oscar application.

## Under Construction ##
The following needs to be added to this application.
+ Support Refunding payments

## License ##
[BSD (Berkeley Software Distribution) License](https://opensource.org/licenses/bsd-license.php).
Copyright (c) 2017, Jorran de Wit.
