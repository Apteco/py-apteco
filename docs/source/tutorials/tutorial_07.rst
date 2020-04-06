**********************************************
  Controlling selection structure and tables
**********************************************

In this part of the tutorial we'll learn
how to control the way a selection is structured and joined together
and how to change which table the selection counts.

Joining more than two selections together
=========================================

We can use the ``&`` ``|`` ``~`` operators we saw in the previous part
to build more complex selections made of multiple parts:

.. code-block:: python

    >>> low_price_deals_audience = eligible_for_discount & ~high_earner

We could have even written the ``eligible_for_discount`` variable directly
using its constituent parts:

.. code-block:: python

    >>> low_price_deals_audience = (student | under_21) & ~high_earner

Here we've had to use parentheses
so that the ``student | under_21`` gets combined first,
before the selection resulting from that is combined with ``~high_earner`` .
Without parentheses, Python's `operator precedence rules
<https://docs.python.org/3/reference/expressions.html#operator-precedence>`_
mean this would be calculated as:

.. code-block:: python

    >>> not_what_we_meant = student | (under_21 & ~high_earner)  # since `&` takes precedence over `|`

Even if operator precedence means that your selection would resolve as intended
without parentheses,
it's probably sensible to include them to be explicit and improve readability:

.. code-block:: python

    >>> either_of_two_pairs = (student & smith) | (high_earner & under_21)

The ``&`` operator 'binds' more tightly than the ``|`` operator,
so this selection would resolve in the same way even if the parentheses were omitted,
but including them makes the logic easier to read
and enables the programmer to communicate their intent.

Determining the resolve table
=============================

The *resolve table* simply refers to the FastStats system table
that the selection is set to count records from.
As mentioned in the previous part, this is determined automatically
according to the following rules:

* for a single 'clause', it is the table that clause's variable belongs to
* for a selection of several clauses,
  it is the table of the first (i.e. left-most) clause

As demonstrated in the following code:

.. code-block:: python

    >>> student = people["peOccu"] == "4"
    >>> usa = bookings["boDest"] == "38"
    >>> student.table_name
    'People'
    >>> usa.table_name
    'Bookings'
    >>> (student & usa).table_name
    'People'
    >>> (usa & student).table_name
    'Bookings'

So if your selection uses elements from different tables,
make sure you begin it with an element from the table
you want to use for the overall count.

Changing the resolve table
==========================

We can also manually change the resolve table of a selection
using the multiplication operator ``*`` with the table:

    >>> been_to_usa = people * usa
    >>> been_to_usa.count()
    273879
    >>> been_to_usa.table_name
    'People'

.. note::

    The table that we 'multiply by' needs to be a ``Table`` object.
    Using the string of the table name will **not** work.

Again, we can use parentheses to group different parts of the selection
to control how it is structured:

.. code-block:: python

    >>> audience_1 = people * (usa & at_least_2k)
    >>> audience_1.count()
    12746
    >>> audience_2 = (people * usa) & at_least_2k
    >>> audience_2.count()
    20098

``audience_1`` selects people who have any booking to the USA costing at least £2000
— the ``usa`` and ``at_least_2k`` clauses are grouped together,
so a person must have a *single* booking matching *both* criteria to be selected.

It is equivalent to this selection in FastStats:

.. figure:: ../_static/audience_1.png
  :scale: 50%
  :align: center

``audience_2`` selects people who have any booking to the USA,
and have any booking costing at least £2000.
The difference is that the conditions don't have to apply to the same booking
— the person's booking to the USA could cost less than £2000,
as long as they have another booking that *does* cost at least that much.

Here's the equivalent selection in FastStats:

.. figure:: ../_static/audience_2.png
  :scale: 50%
  :align: center

That's the end of the tutorial!
Hopefully you're now equipped with the knowledge you need
to build and count your own selections.
Check out the rest of the documentation for more guidance,
and if you have any questions,
don't hesitate to `get in touch <mailto:support@apteco.com>`_.
