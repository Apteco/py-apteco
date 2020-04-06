*******************************************
  Selecting with different variable types
*******************************************

In this part of the tutorial we'll learn
what kind of values you can specify when making selections
with different types of FastStats variables.

Selector, Array & Flag Array
============================

As mentioned in the previous part, FastStats **Selector** variables
require selector codes given as strings (Python ``str`` type).

This is also true for **Array** and **Flag Array** variables:

.. code-block::

    >>> households = my_session.tables["Households"]
    >>> ford_owners = households["HHCarmak"] == "FOR"
    >>> ford_owners.count()
    51614
    >>> broadsheet_readers = people["peNews"] == [
    ...     "Financial Times",
    ...     "The Times",
    ...     "Daily Telegraph",
    ...     "The Guardian",
    ...     "Independent",
    ... ]
    >>> broadsheet_readers.count()
    531936

.. note::

    Even selector codes that are numerical in form must be given
    as their string equivalents with appropriate 0-padding,
    as in the *high earners* example in the previous part.

Numeric
=======

**Numeric** variables accept any number type:

.. code-block:: python

    >>> policies = my_session.tables["Policies"]
    >>> ten_days_until_travel = policies["PoDaysUn"] == 10
    >>> ten_days_until_travel.count()
    5085
    >>> premium_87_65 = policies["PoPremiu"] == 87.65
    >>> premium_87_65.count()
    8

As well as ``int`` and ``float`` types, you can use other numerical types
like ``Decimal`` from the built-in ``decimal`` module:

    >>> from decimal import Decimal
    >>> cost12345 = bookings["boCost"] == Decimal("123.45")
    >>> cost12345.count()
    11

Text
====

**Text** variables use Python strings:

.. code-block:: python

    >>> smiths = people["peSName"] == "Smith"
    >>> smiths.count()
    13302
    >>> vowel_initial = people["peInit"] == list("AEIOU")
    >>> vowel_initial.values
    ['A', 'E', 'I', 'O', 'U']
    >>> vowel_initial.count()
    168548

Date & DateTime
===============

**Date** and **DateTime** variables use the built-in Python ``datetime.date``
and ``datetime.datetime`` types.

.. code-block:: python

    >>> from datetime import date
    >>> christmas_day_2019 = bookings["boDate"] == date(2019, 12, 25)
    >>> christmas_day_2019.count()
    627
    >>> travel_on_1st = bookings["boTrav"] == [
    ...     date(y, m, 1)
    ...     for y in range(2016, 2020)
    ...     for m in range(1, 13)
    ... ]
    >>> travel_on_1st.count()
    41660

FastStats does not support picking a single date-time directly,
so we can't use the ``==`` operator as we have with other variable types here.
But in the next part we'll learn other ways to make selections,
including using **DateTime** variables.
