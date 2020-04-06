**********************************
  Accessing tables and variables
**********************************

In this part of the tutorial we'll learn
about accessing some of the core objects from your FastStats system
— tables and variables.

Tables
======

The FastStats system tables are accessible via the ``tables`` attribute
on the ``Session``, which returns a Python dictionary,
with the table names as keys which map to a ``Table`` object representing the table.

This example loops through the tables and prints each one's name:

.. code-block:: python

    >>> for table in my_session.tables.values():
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

You can retrieve a specific table from the dictionary using its name:

.. code-block:: python

    >>> bookings = my_session.tables["Bookings"]

The ``Table`` objects have several attributes with information about the table:

.. code-block:: python

    >>> print(
    ...     f"There are {bookings.total_records:,}"
    ...     f" {bookings.plural_display_name.lower()}"
    ...     f" in the system."
    ... )
    ...
    There are 2,130,081 bookings in the system.

Variables
=========

The FastStats system variables are similarly stored in a dictionary
at the ``variables`` attribute on the ``Session``.
The keys of the dictionary are variable names
and the values are ``Variable`` objects which represent the variable.

You can retrieve a variable from the dictionary using its name:

.. code-block:: python

    >>> cost = my_session.variables["boCost"]

The ``Variable`` object has attributes providing information about the variable:

.. code-block:: python

    >>> cost.description
    'Cost'
    >>> cost.type
    'Numeric'

Each table also has a ``variables`` attribute,
which returns a dictionary containing just the variables on that table:

.. code-block:: python

    >>> all_vars = my_session.variables
    >>> len(all_vars)
    94
    >>> bookings_vars = bookings.variables
    >>> len(bookings_vars)
    14

The variables on the table can be accessed by name in the same way:

.. code-block:: python

    >>> destination = bookings.variables["boDest"]
    >>> destination.type
    'Selector'

A variable's attributes differ according to its type:

.. code-block:: python

    >>> cost.currency_symbol
    '£'
    >>> destination.num_codes
    20

Here, ``cost`` is a Numeric variable
representing an amount of British Pounds Sterling (£),
and ``destination`` is a selector variable with 20 different selector codes.

At the moment we've only seen how to access our variables and their attributes,
but in the next part we'll learn how to use them to build selections.
