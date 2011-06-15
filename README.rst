============
django-payme
============

Fully portable Django payments application
==========================================

Inspired by mamona, django-payme is yet another payment app for Django that
attempts to solve the problem of accepting payments as a merchant.

There aren't really any docs yet, because the architecture is still some-what
in flux. Stay tuned.


Installation
============

1. Install django-payme: ``pip install django-payme``
2. Add the app to your Django project::

    INSTALLED_APPS = (
        ...
        'payme',
    )

3. Modify your URLconf to hook in django-payme::

    import payme

    urlpatterns = patterns('',
        ...
        (r'^payme/', include(payme.urls))
    )
