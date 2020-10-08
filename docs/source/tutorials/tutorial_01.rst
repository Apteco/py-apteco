***************************************
  Connecting to your FastStats system
***************************************

In this part of the tutorial we'll learn
about creating a connection to your FastStats system.

Make sure you have **py-apteco** installed before you start
— see the :doc:`installation guide <../install>` for instructions.

Logging in
==========

To get started, import the :func:`login` function from the :mod:`apteco` package.
You can then connect to your FastStats system by calling the function
with the following credentials as arguments:

* **API base URL**: the URL for your Apteco API (Orbit API) installation
* **DataView name**: the name of the DataView you're connecting to
* **FastStats system name**: the name of the system you're using within the Dataview
* **Username**: your username (the same as you use to log in to Orbit)

.. todo::

    add methods & classes to ``apteco.__init__``

.. code-block:: python

   >>> from apteco import login
   >>> my_session = login("https://my-site.com/OrbitAPI", "my_data_view", "my_system", "jdoe")

If you're working in the terminal, you'll be asked to enter your password,
which won't be visible as you type it.
If Python can't prevent your password from appearing like this,
or if you're running an application,
a pop-up password entry box will appear for you to use instead.
This might appear in the background,
so check your taskbar for a new window if nothing seems to be happening.

If you don't want to enter your password every time,
there is also a :func:`login_with_password` function which takes your password
as a fifth argument:

.. code-block:: python

   >>> from apteco import login_with_password
   >>> my_session = login_with_password(
   ...     "https://my-site.com/OrbitAPI", "my_data_view", "my_system", "jdoe", "password"
   ... )

.. warning::
    It is not considered good practice to have passwords saved within code like this
    — be aware of the security implications if doing so.


Checking your session
=====================

To verify that the login was successfully,
you can inspect the information about the FastStats system
the session is connected to:

.. code-block:: python

    >>> sys_info = my_session.system_info
    >>> print(
    ...     f"Connected to {sys_info.description}"
    ...     f", built on {sys_info.build_date.strftime('%d %B %Y at %X')}."
    ... )
    ...
    Connected to Holidays Demo Database, built on 27 November 2019 at 15:57:24.

The :class:`Session` object holds more than just this metadata
about the FastStats system,
and in the next part we'll learn how to access the system Tables and Variables.
