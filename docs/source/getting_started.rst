Quickstart
==========

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

   python -m pip install apteco

Logging in
----------

Your login credentials are the same username and password
you would use to log in to Apteco Orbit™:

.. code-block:: python

    >>> from apteco import login
    >>> my_session = login("https://my-site.com/OrbitAPI", "my_data_view", "my_system", "jdoe")

You will be asked to enter your password in the terminal, which won't be echoed.
If Python is unable to ask for your password in this way,
it will provide a pop-up box instead.
This might appear in the background,
so check your taskbar for a new window if nothing seems to be happening.

If you don't want to enter your password every time,
there's also a :func:`login_with_password` function which takes your password
as a fifth argument:

.. code-block:: python

    >>> from apteco import login_with_password
    >>> my_session = login_with_password(
    ...     "https://my-site.com/OrbitAPI",
    ...     "my_data_view",
    ...     "my_system",
    ...     "jdoe",
    ...     "password",  # password is in plain sight in the code!
    ... )

Tables
------

Tables are accessed through the :attr:`tables` attribute on the :class:`Session` object.
You can retrieve a table using its name:

.. code-block:: python

    >>> bookings = my_session.tables["Bookings"]

:class:`Table` objects have properties for various metadata:

.. code-block:: python

    >>> print(
    ...     f"There are {bookings.total_records:,}"
    ...     f" {bookings.plural_display_name.lower()}"
    ...     f" in the system."
    ... )
    There are 2,130,081 bookings in the system.

Variables
---------

Variables are accessed through the :attr:`variables` attribute
on the :class:`Session` object.
You can retrieve a variable using its name or description:

.. code-block:: python

    >>> surname = my_session.variables["peSName"]  # name
    >>> cost = my_session.variables["Cost"]  # description

Each table also has a :attr:`variables` attribute
for accessing the variables on that table:

.. code-block:: python

    >>> destination = bookings.variables["Destination"]

For convenience you can access variables by indexing into the :class:`Table` itself:

.. code-block:: python

    >>> destination = bookings["Destination"]

:class:`Variable` objects have attributes with various metadata:

.. code-block:: python

    >>> cost.description
    'Cost'
    >>> destination.type
    'Selector'

Creating selections
-------------------

You can use the Python operators with :class:`Variable` objects to build selections
based on criteria and return a count:

.. code-block:: python

    >>> sweden = bookings["Destination"] == "29"
    >>> sweden.count()
    25207

You can specify multiple values using any *iterable*:

.. code-block:: python

    >>> people = my_session.tables["People"]
    >>> high_earners = people["Income"] == (f"{i:02}" for i in range(7, 12))
    >>> high_earners.count()
    7114

You can use other operators as well; for example, to exclude values:

.. code-block:: python

    >>> uk_only = households["Region"] != "14"  # 14 is Channel Islands
    >>> uk_only.count()
    741572

Or to allow a range of values:

.. code-block:: python

    >>> low_profit = bookings["Profit"] <= 25
    >>> low_profit.count()
    211328

.. code-block:: python

    >>> second_half_of_alphabet = people["Surname"] >= "N"
    >>> second_half_of_alphabet.count()
    410954

Date and DateTime variables use the built-in :mod:`datetime` module:

.. code-block:: python

    >>> from datetime import date, datetime
    >>> bookings_before_2019 = bookings["Booking Date"] <= date(2018, 12, 31)
    >>> bookings_before_2019.count()
    972439

You can take advantage of functionality available in other Python packages:

.. code-block:: python

    >>> from dateutil.relativedelta import relativedelta
    >>> under_30 = people["DOB"] >= date.today() - relativedelta(years=30)
    >>> under_30.count()
    207737

Combining selections
--------------------

You can use the ``&`` ``|`` operators to combine selection criteria:

.. code-block:: python

    >>> sweden = bookings["Destination"] == "29"
    >>> cost_at_least_2k = bookings["Cost"] >= 2000
    >>> expensive_sweden = sweden & cost_at_least_2k
    >>> expensive_sweden.count()
    632
    >>> student = people["Occupation"] == "4"
    >>> under_21 = people["DOB"] >= date.today() - relativedelta(years=21)
    >>> eligible_for_discount = student | under_21
    >>> eligible_for_discount.count()
    188364

The ``~`` operator negates a selection:

.. code-block:: python

    >>> pay_full_price = ~eligible_for_discount
    >>> pay_full_price.count()
    968189

You can join clauses from different tables and it will automatically handle
the required table changes:

.. code-block:: python

    >>> high_affordability = high_earners | cost_at_least_2k  # will resolve to people
    >>> high_affordability.count()
    56096
    >>> high_affordability.table_name
    'People'

The left-most clause determines the resolve table:

.. code-block:: python

    >>> female = people["Gender"] == "F"
    >>> usa = bookings["Destination"] == "38"
    >>> female.table_name
    'People'
    >>> usa.table_name
    'Bookings'
    >>> (female & usa).table_name
    'People'
    >>> (usa & female).table_name
    'Bookings'

You can manually set the resolve table using the ``*`` operator:

.. code-block:: python

    >>> bookings_by_under_21s = bookings * under_21
    >>> bookings_by_under_21s.count()
    135100
    >>> bookings_by_under_21s.table_name
    'Bookings'

Compound clauses follow Python operator precedence:

.. code-block:: python

    >>> student_or_young_female = student | female & under_21
    >>> student_or_young_female.count()
    166708
    >>> student_or_female_must_be_young = (student | female) & under_21
    >>> student_or_female_must_be_young.count()
    49225

Be especially careful where compound clauses involve table changes:

.. code-block:: python

    >>> women_to_sweden = female & sweden
    >>> women_to_sweden.count()  # selection on People table
    8674
    >>> audience_1 = bookings * (female & sweden)
    >>> audience_1.count()  # bookings by women who've been to sweden
    23553
    >>> audience_2 = (bookings * female) & sweden
    >>> audience_2.count()  # bookings made by a woman, with destination of sweden
    8687

For a more thorough introduction, check out the :ref:`tutorial`.
