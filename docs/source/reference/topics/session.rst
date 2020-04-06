***********
  Session
***********

.. module:: session.Session

Introduction
============

The ``Session`` object is central to the `apteco` package.
It is the 'key' for connecting to the Apteco API,
so performs a similar role to an API Client object in other API wrapper packages
(see `py-trello <https://github.com/sarumont/py-trello/blob/40df9e69010b4860ad40a7627eba3331d9c97185/trello/trelloclient.py#L28>`_,
`PyGitHub <https://pygithub.readthedocs.io/en/latest/github.html>`_).
But as well as handling API requests
it also holds a copy of the core data for the FastStats system it is connected to,
similar to the *System* tab within the Apteco FastStats desktop application.
This lets you easily access FastStats tables and variables
to perform data analysis quickly.

As you carry out your analysis, fetching different FastStats objects,
creating selections and producing other results,
each object is passed a reference to the current active Session object,
so you can use any of these as the starting point for further analysis
without having to reconnect to the Apteco API.

Basic use
=========

Logging in by entering your password in the terminal (it won't be echoed)::

    >>> from apteco.session import login
    >>> my_session = login("https://orbit.my-site.com/OrbitAPI", "my_data_view", "my_system", "jdoe")
    Enter your password:

Logging in by giving your password in the function call::

    >>> from apteco.session import login_with_password
    >>> my_session = login_with_password(
            "https://orbit.my-site.com/OrbitAPI",
            "my_data_view",
            "my_system",
            "jdoe",
            "P@ssw0rd123!",  # Beware - password is visible in the code!
        )

Accessing tables and variables::

    >>> people = my_session.tables["People"]
    >>> cost = my_session.variables["Cost"]

Serializing and deserializing the session::

    >>> s = my_session.serialize()
    >>> from apteco.session import Session
    >>> my_restoed_session = Session.deserialize(s)

.. Ending a session::
..
..     >>> my_session.logout()
..

Session-related tasks
=====================

.. currentmodule:: apteco.session

Creating a session
------------------

To create a session, call the :class:`login` function with the appropriate credentials.
You will then be asked to enter your password in the terminal (which won't be echoed)
or if this isn't possible, a pop-up box will appear for it.
To give your password directly instead, use the :class:`login_with_password` function
which takes your password as an argument to the function call.

Both these functions return an authenticated :class:`Session` object
connected to the chosen FastStats system.

.. note::
    It is not currently possible to create a session
    by calling the :class:`Session` class directly.

Serializing and de-serializing a session
----------------------------------------

.. currentmodule:: apteco.session.Session

Call the :attr:`serialize` method on a session object
to serialize it down to a string.

.. currentmodule:: apteco.session

To deserialize it, use the static method :attr:`Session.deserialize`,
passing in the serialized string.

.. warning::
    Be careful where and how you store the serialized string.
    As long as the session remains valid,
    anyone with a copy of the string and access to your installation of the Apteco API
    will be able to access your FastStats system.

.. Ending a session
.. ----------------
..
.. Call the :attr:`logout` method on a session object to end the session
.. and disconnect from the Apteco API.

API reference
=============

Login functions
---------------

.. currentmodule:: apteco.session

These are functions in the :mod:`apteco.session` module,
and can be called to log in to the Apteco API and return a :class:`Session` object.

.. py:function:: login(base_url: str, data_view: str, system: str, user: str)

    Return a :class:`Session` object connected to the given FastStats system.

    You will be asked to enter your password in the terminal.
    If you are not using a terminal,
    or Python is not able to prevent your password from being echoed,
    a pop-up box will be opened where you can enter your password instead.

.. py:function:: login_with_password(base_url: str, data_view: str, system: str, user: str, password: str)

    Return a :class:`Session` object connected to the given FastStats system.

    This function is identical to the previous :class:`login` function,
    but with an additional fifth argument in the function call
    for you to enter your password directly.

    .. warning ::
        Be mindful of security when using this function
        and avoid storing passwords in plain text in code files.

Apteco API session properties
-----------------------------

These attributes on the :class:`Session` object
are the core pieces of data that identify the Apteco API instance
which it's connected to.

.. currentmodule:: apteco.session.Session

.. py:data:: base_url

    URL for your Apteco API (Orbit API) installation

.. py:data:: data_view

    name of the DataView you’re connected to

.. py:data:: system

    name of the system you’re using within the Dataview

.. py:data:: access_token

    token used to authenticate with the API (this is a `JWT <https://jwt.io/>`_)

.. py:data:: session_id

    traditional FastStats session ID

.. py:data:: api_client

    :class:`apteco-api.ApiClient` object which handles all the API requests,
    using the `apteco-api` package

FastStats system metadata
-------------------------

These attributes on the :class:`Session` object
contain metadata about the FastStats system the object is connected to.

.. py:data:: system_info

    :class:`namedtuple` representing the FastStats system,
    with the following attributes:

    * **name** (:class:`str`): system name
    * **description** (:class:`str`): system description
    * **build_date** (:class:`datetime.datetime`): date the system was build
    * **view_name** (:class:`str`): DataView the system belongs to

.. py:data:: user

    :class:`namedtuple` representing the user, with the following attributes:

    * **username** (:class:`str`): username (used to log in)
    * **first_name** (:class:`str`): user's first name
    * **surname** (:class:`str`): user's surname
    * **email_address** (:class:`str`): user's email address

Tables and Variables
--------------------

These attributes on the :class:`Session` object
provide access to the tables and variables data
for the FastStats system the object is connected to.

.. py:data:: tables

    A :class:`dict` mapping table names their corresponding ``Table`` object

    >>> my_session.tables["Communications"]
    <apteco.session.Table object at 0x0000020FC2E5A240>

    .. tip::
        You may find it helpful to allocate commonly-used tables to Python variables
        at the beginning your script or interactive session
        for easier use and reference::

        >>> households = my_session.tables["Households"]
        >>> people = my_session.tables["People"]
        >>> bookings = my_session.tables["Bookings"]

.. py:data:: master_table

    :class:`Table` object of the master (root) table

    >>> master = my_session.master_table
    >>> master
    <apteco.session.Table object at 0x0000020FC2C9D400>
    >>> master.name
    'Households'

.. py:data:: variables

    A :class:`dict` mapping table names their corresponding ``Variable`` object

    >>> my_session.variables["Cost"]
    <apteco.session.SelectorVariable object at 0x0000020FC2E83DD8>
    >>> my_session.variables["Occupation"].name
    'peOccu'

    .. note::
        You can also retrieve variables from their respective ``Table`` object.

    .. tip::
        You may find it helpful to allocate commonly-used FastStats variables
        to Python variables at the beginning your script or interactive session
        for easier use and reference

        >>> dest = my_session.variables["Destination"]
        >>> dest.name, dest.type, dest.is_virtual
        ('boDest', 'Selector', False)
