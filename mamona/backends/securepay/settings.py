"""
SecurePay specific settings.

Available settings are in __all__, and are added module-level variables when
this module is first imported.

Example::

    >>> from mamona.backends.securepay import settings
    >>> settings.URL
    sandbox = "https://vault.safepay.com.au/cgi-bin/test_payment.pl"

Values for these settings are configurable via the mamona backend settings in
the project's ``settings.py``::

    MAMONA_BACKEND_SETTINGS = {
        "securepay": {
            "URL": "abcd",
        }
    }

"""
import sys
from mamona import settings


__all__ = (
    "URL",
    "FORM_VENDOR_NAME",
    "FORM_BACKGROUND_IMAGE",
    "FORM_BUTTON_RESET",  # text to display on the reset button
    "FORM_BUTTON_SUBMIT",  # text to display on the reset button
    "FORM_CARDS_ACCEPTED",
    "FORM_COLOUR_ALINK",
    "FORM_COLOUR_LINK",
    "FORM_COLOUR_PAGE",
    "FORM_COLOUR_TABLE",
    "FORM_COLOUR_TEXT",
    "FORM_COLOUR_VLINK",
    "FORM_CURRENCY",
    "FORM_FONT",
    "FORM_GST_RATE",
    "FORM_GST_ADDED",
    "FORM_GST_EXEMPT_FIELDS",
    "FORM_HEADING_ORDER",
    "FORM_HEADING_PAGE",
    "FORM_HEADING_PRICE",
    "FORM_HEADING_PRODUCT",
    "FORM_HEADING_UNIT",
    "FORM_HEADING_UNIT_PRICE",
    "FORM_PAYMENT_ALERT",
    "FORM_PAYMENT_REFERENCE",
    "FORM_PRINT_ZERO_QTY",
    "FORM_RECEIPT_ADDRESS",
    "FORM_RETURN_LINK_TEXT",
    "FORM_RETURN_LINK_URL",
    "FORM_REPLY_LINK_URL",
    "FORM_SPACING_FIELD_NAMES",
    "FORM_TABLE_BORDER",
    "FORM_TABLE_PADDING",
    "FORM_TABLE_SPACING",
    "FORM_TABLE_WIDTH",
)

mod = sys.modules[__name__]
user_defined = settings.BACKENDS_SETTINGS.get("securepay", {})

# create module-level variables for each of the fields, favouring user defined
# settings for this backend, and falling back to the built-in defaults defined
# above.
for field in __all__:
    setattr(mod, field, user_defined.get(field, defaults.get(field)))

# All the module-level variables have been setup, let's set a default value for
# URL based on USE_SANDBOX
if mod.URL is None:
    live = "https://vault.safepay.com.au/cgi-bin/make_payment.pl"
    sandbox = "https://vault.safepay.com.au/cgi-bin/test_payment.pl"
    mod.URL = sandbox if settings.USE_SANDBOX else live