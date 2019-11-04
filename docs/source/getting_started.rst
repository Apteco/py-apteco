Getting Started
===============

Requirements
------------

* Python 3.6+
* Access to an installation of the Apteco API

The Apteco API (which also goes under the name **Orbit API**)
is part of the Apteco Orbit™ installation.
If you have access to Apteco Orbit™, you also have access to the Apteco API!
If you're not sure about this, contact whoever administers your Apteco software,
or get in touch with Apteco support (support@apteco.com).

Installation
------------

You can install the package the usual way from PyPI using ``pip``:

.. code-block:: console

   pip install apteco

Logging in
----------

Your login credentials are the same username and password
you would use to log in to Apteco Orbit™:

.. code-block:: python

   from apteco.session import login, Session

   credentials = login("https://my-site.com/OrbitAPI", "my_data_view", "jdoe")
   holidays = Session(credentials, "holidays")

You will be asked to enter your password in the terminal, which won't be echoed.
If Python is unable to ask for your password in this way,
it will provide a pop-up box instead.
This might appear in the background,
so check your taskbar for a new window if nothing seems to be happening.

If you don't want to enter your password every time,
there is also a ``login_with_password()`` function which takes your password
as a fourth argument:

.. code-block:: python

   from apteco.session import login_with_password

   # password is in plain sight in the code!
   credentials = login_with_password(
       "https://my-site.com/OrbitAPI", "my_data_view", "jdoe", "password"
   )
   holidays = Session(credentials, "holidays")

