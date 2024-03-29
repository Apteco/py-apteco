***********
  Session
***********

.. py:currentmodule:: apteco.session

Introduction
============

The :class:`Session` object is central to the `apteco` package.
It is the 'key' for connecting to the Apteco API,
so performs a similar role to an API Client object in other API wrapper packages
(see `py-trello <https://github.com/sarumont/py-trello/blob/40df9e69010b4860ad40a7627eba3331d9c97185/trello/trelloclient.py#L28>`_,
`PyGitHub <https://pygithub.readthedocs.io/en/latest/github.html>`_).
But as well as handling API requests
it also holds a copy of the core data for the FastStats system it is connected to,
similar to the `System` tab within the Apteco FastStats desktop application.
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

    >>> from apteco import login
    >>> my_session = login("https://orbit.my-site.com/OrbitAPI", "my_data_view", "my_system", "jdoe")
    Enter your password:

Logging in by giving your password in the function call::

    >>> from apteco import login_with_password
    >>> my_session = login_with_password(
    ...     "https://orbit.my-site.com/OrbitAPI",
    ...     "my_data_view",
    ...     "my_system",
    ...     "jdoe",
    ...     "P@ssw0rd123!",  # Beware - password is visible in the code!
    ... )

Accessing tables and variables::

    >>> people = my_session.tables["People"]
    >>> cost = my_session.variables["Cost"]

Serializing and deserializing the session::

    >>> s = my_session.serialize()
    >>> from apteco import Session
    >>> my_restored_session = Session.deserialize(s)

.. Ending a session::
..
..     >>> my_session.logout()
..

Session-related tasks
=====================

.. currentmodule:: apteco

Creating a session
------------------

To create a session, call the :func:`login` function with the appropriate credentials.
You will then be asked to enter your password in the terminal (which won't be echoed)
or if this isn't possible, a pop-up box will appear for it.
To give your password directly instead, use the :func:`login_with_password` function
which takes your password as an argument to the function call.

Both these functions return an authenticated :class:`Session` object
connected to the chosen FastStats system.

.. note::
    It is not currently possible to create a session
    by calling the :class:`Session` class directly.

Serializing and de-serializing a session
----------------------------------------

.. currentmodule:: apteco.session.Session

Call the :meth:`serialize` method on a session object
to serialize it down to a string.

.. currentmodule:: apteco.session

To deserialize it, use the static method :meth:`Session.deserialize`,
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

.. module:: apteco

These functions can be imported directly from :mod:`apteco`,
and can be called to log in to the Apteco API and return a :class:`Session` object.

.. py:function:: login(base_url: str, data_view: str, system: str, user: str)

    Return a :class:`Session` object connected to the given FastStats system.

    :param str base_url: API base URL, normally ending '/OrbitAPI'
    :param str data_view: DataView being logged into
    :param str system: FastStats system to connect to
    :param str user: username of API user

    You will be asked to enter your password in the terminal.
    If you are not using a terminal,
    or Python is not able to prevent your password from being echoed,
    a pop-up box will be opened where you can enter your password instead.

.. py:function:: login_with_password(base_url: str, data_view: str, system: str, user: str, password: str)

    Return a :class:`Session` object connected to the given FastStats system.

    :param str base_url: API base URL, normally ending '/OrbitAPI'
    :param str data_view: DataView being logged into
    :param str system: FastStats system to connect to
    :param str user: username of API user
    :param str password: password for this user

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

.. py:attribute:: Session.base_url

    URL for your Apteco API (Orbit API) installation

.. py:attribute:: Session.data_view

    name of the DataView you’re connected to

.. py:attribute:: Session.system

    name of the system you’re using within the DataView

.. py:attribute:: Session.access_token

    token used to authenticate with the API (this is a `JWT <https://jwt.io/>`_)

.. py:attribute:: Session.session_id

    traditional FastStats session ID

.. py:attribute:: Session.api_client

    :class:`apteco-api.ApiClient` object which handles all the API requests,
    using the :mod:`apteco-api` package

FastStats system metadata
-------------------------

These attributes on the :class:`Session` object
contain metadata about the FastStats system the object is connected to.

.. py:attribute:: Session.system_info

    :class:`namedtuple` representing the FastStats system,
    with the following attributes:

    * **name** (`str`): system name
    * **description** (`str`): system description
    * **build_date** (`datetime.datetime`): date the system was build
    * **view_name** (`str`): DataView the system belongs to

.. py:attribute:: Session.user

    :class:`namedtuple` representing the user, with the following attributes:

    * **username** (`str`): username (used to log in)
    * **first_name** (`str`): user's first name
    * **surname** (`str`): user's surname
    * **email_address** (`str`): user's email address

Tables and Variables
--------------------

These attributes on the :class:`Session` object
provide access to the tables and variables data
for the FastStats system the object is connected to.

.. py:attribute:: Session.tables

    An object providing both list-like and dict-like access to tables.
    Tables can be looked up by name to retrieve their corresponding
    :class:`Table` object::

        >>> my_session.tables["Communications"]
        <apteco.tables.Table object at 0x0000020FC2E5A240>

    You can also count the tables using the built-in :func:`len` function
    and iterate over them::

        >>> len(my_session.tables)
        9
        >>> for table in holidays.tables:
        ...     print(f"{table.total_records:>9,} {table.plural}")
        ...
          742,565 Households
        1,156,553 People
        2,130,081 Bookings
          213,567 Policies
          279,538 WebVisits
           70,705 Communications
           55,653 Journeys
          153,041 Content
            1,549 Responses

    .. tip::
        You may find it helpful to allocate commonly-used tables to Python variables
        at the beginning your script or interactive session
        for easier use and reference::

        >>> households = my_session.tables["Households"]
        >>> people = my_session.tables["People"]
        >>> bookings = my_session.tables["Bookings"]

    .. seealso::
        Refer to the :ref:`tables_reference` documentation for more details
        on using table objects.

.. py:attribute:: Session.master_table

    :class:`Table` object of the master (root) table

    >>> master = my_session.master_table
    >>> master
    <apteco.session.Table object at 0x0000020FC2C9D400>
    >>> master.name
    'Households'

.. py:attribute:: Session.variables

    An object providing both list-like and dict-like access to variables.
    Variables can be looked up by name or description to retrieve their
    corresponding :class:`Variable` object::

        >>> my_session.variables["peOccu"]
        <apteco.variables.SelectorVariable object at 0x0000020FC2E83DD8>
        >>> my_session.variables["Destination"].name
        'boDest'

    .. note::
        Variables are also accessible through their respective :class:`Table` object.
        See the :ref:`Tables documentation <table_variables>` for details.

    Variables can be counted using the built-in :func:`len` function
    and you can also iterate over them::

        >>> len(my_session.variables)
        94
        >>> for var in my_session.variables:
        ...     if "date" in var.description.lower():
        ...         print(f"{var.name:>8}: {var.description}")
        ...
          boDate: Booking Date
          boTrav: Travel Date
        bo1O9ZTR: Busy dates
        PoPolic1: Policy Date
        PoTrave1: Policy Travel Date
        PoBooki1: Policy Booking Date
        cmCommDt: Date of Communication
        raRspDat: Response Date
        ReCommun: Communication Date

    .. seealso::
        Refer to the :ref:`variables_reference` documentation for more details
        on using variable objects.
