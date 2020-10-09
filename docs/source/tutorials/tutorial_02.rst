**********************************
  Accessing tables and variables
**********************************

In this part of the tutorial we'll learn
about accessing some of the core objects from your FastStats system
— tables and variables.

Tables
======

The FastStats system tables are accessible via the :attr:`tables` attribute
on the :class:`Session`.
This is a single object which provides both list-like and dict-like
access to the :class:`Table` objects representing the tables.

You can retrieve a specific table using its name:

.. code-block:: python

    >>> bookings = my_session.tables["Bookings"]

You can loop through the tables:

.. code-block:: python

    >>> for table in my_session.tables:
    ...     print(table.name)
    ...
    Households
    People
    Bookings
    Policies
    WebVisits
    Communications
    Journey History
    Content
    Responses Attributed

You can use the built-in :func:`len` function to count them:

.. code-block:: python

    >>> len(my_session.tables)
    9

The :class:`Table` objects have various attributes for the table's metadata:

.. code-block:: python

    >>> print(
    ...     f"There are {bookings.total_records:,}"
    ...     f" {bookings.plural_display_name.lower()}"
    ...     f" in the system."
    ... )
    ...
    There are 2,130,081 bookings in the system.

.. seealso::
    See the :ref:`tables_reference` reference guide for full details
    of the :class:`Table` metadata attributes.

Variables
=========

The FastStats system variables are similarly accessible
through the :attr:`variables` attribute on the :class:`Session`.
You can retrieve a variable using its name or description:

.. code-block:: python

    >>> surname = my_session.variables["peSName"]
    >>> cost = my_session.variables["Cost"]

Each :class:`Table` also has a :attr:`variables` attribute which works in the same way,
providing access to the variables on that table:

.. code-block:: python

    >>> booking_date = bookings.variables["boDate"]
    >>> destination = bookings.variables["Destination"]

For convenience you can also just index into the :class:`Table` object itself:

.. code-block:: python

    >>> booking_date = bookings["boDate"]
    >>> destination = bookings["Destination"]

As with :attr:`tables` above,
:attr:`variables` also supports counting using :func:`len`, and looping:

.. code-block:: python

    >>> len(my_session.variables)
    94
    >>> len(bookings.variables)
    14
    >>> for var in bookings.variables:
    ...     if var.type == "Numeric":
    ...         print(var.description)
    ...
    Cost
    Profit

The :class:`Variable` objects have attributes with metadata for the variable.

.. code-block:: python

    >>> cost.type
    'Numeric'
    >>> cost.currency_symbol
    '£'
    >>> destination.type
    'Selector'
    >>> destination.num_codes
    20

Here, ``cost`` is a **Numeric** variable
representing an amount of British Pounds Sterling (£),
and ``destination`` is a **Selector** variable with 20 different selector codes.

.. note::
    Some attributes are common to all variables,
    while others vary according to the variables type.
    For full details see the :ref:`variables_reference` reference guide.

At the moment we've only seen how to access our variables and their attributes,
but in the next part we'll learn how to use them to build selections.
