Getting Started
===============

Requirements
------------

* Python 3.6+
* Access to an installation of the Apteco API

The Apteco API, which also goes under the name **Orbit API**,
is part of the Apteco Orbit™ installation.
If you have access to Apteco Orbit™, you also have access to the Apteco API!
If you're not sure about this, contact whoever administers your Apteco software,
or get in touch with Apteco support.

Installation
------------

You can install the package the usual wat from PyPI using ``pip``::

   pip install py-apteco

Then import the package::

   import apteco

.. note::

   The package name, which is used for installation, is ``py-apteco``,
   but the module name used for importing is just ``apteco``.

Logging in
----------

Your login credentials are the same username and password
you would use to log in to Apteco Orbit™::

   import apteco as apt

   credentials = apt.login("https://my-site.com/OrbitAPI", "my_data_view", "jdoe")
   holidays = apt.Session(credentials, "holidays")

You will be asked to enter your password in the terminal, which won't be echoed.
If Python is unable to ask for your password in this way,
it will provide a pop-up box instead.
This might appear in the background,
so check your taskbar for a new window if nothing seems to be happening.

If you don't want to enter your password every time,
there is also a ``login_with_password()`` function which takes your password
as a fourth argument::

   # password is in plain sight in the code!
   credentials = apt.login_with_password(
       "https://my-site.com/OrbitAPI", "my_data_view", "jdoe", "password"
   )

