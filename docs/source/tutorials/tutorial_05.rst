*******************************
  Specifying selection values
*******************************

In this part of the tutorial we'll learn
other ways of specifying the values within selections.

Excluding values from selections
================================

So far we've always specified the values we want to *include* in our selections.
But just as in the FastStats application,
we can also choose what values we want to *exclude* instead.
We do this using the Python 'not equal' operator ``!=`` :

.. code-block:: python

    >>> uk_only = households["Region"] != "14"
    >>> uk_only.count()
    741572

(``14`` is the selector code for the Channel Islands region,
so this a selection of all households in the UK 'proper')

.. hint::

    Just as with the ``==`` operator seen in previous examples,
    instead of performing a comparison,
    the ``!=`` operator has been 'overloaded' to create a selection
    but with the :attr:`include` flag set to :const:`False`
    — to *exclude* the given value.

    .. code-block:: python

        >>> type(uk_only)
        <class 'apteco.query.SelectorClause'>
        >>> uk_only.values
        ['14']
        >>> uk_only.include
        False

We can also specify multiple values to exclude:

    >>> england = households["Region"] != ["10", "11", "12", "14"]
    >>> england.count()
    627550

(``10``, ``11``, ``12``, ``14`` are the selector codes for
Scotland, Wales, Northern Ireland & Channel Islands)

You can use the ``!=`` operator everywhere that you can use ``==`` .

Specifying ranges of values
===========================

As well as choosing one or more specific values,
some variables also allow you to choose a whole range of values
using the Python inequality operators ``<=`` and ``>=`` :

Numeric ranges
--------------

.. code-block:: python

    >>> at_least_2k = bookings["Cost"] >= 2000
    >>> at_least_2k.count()
    53267
    >>> low_profit = bookings["Profit"] <= 25
    >>> low_profit.count()
    211328

**Numeric** variables also support the *strict* inequality operators
``<`` and ``>`` .

.. note::

    Unlike the ``==`` and ``!=`` operators,
    the inequality operators only accept a single value.

    If necessary, you can use the Python built-in :func:`max` or :func:`min` function
    to pick out the appropriate value to use for your selection.

Date & DateTime ranges
----------------------

We can use inequality operators to create a selection with a range of dates or times:

.. code-block:: python

    >>> from datetime import date, datetime
    >>> bookings_before_2019 = bookings["Booking Date"] <= date(2018, 12, 31)
    >>> bookings_before_2019.count()
    972439
    >>> web_visits = my_session.tables["WebVisits"]
    >>> website_launch = datetime(2019, 5, 11, 15, 12, 36)
    >>> visits_to_new_site = web_visits["Web Visit Time"] >= website_launch
    >>> visits_to_new_site.count()
    133564

Because **Date** and **DateTime** variables use
:class:`datetime.date` and :class:`datetime.datetime` objects,
we can take advantage of functionality available for working with these.
For example, using the popular :mod:`dateutil` package:

.. code-block:: python

    >>> from dateutil.relativedelta import relativedelta
    >>> under_30 = people["DOB"] >= date.today() - relativedelta(years=30)
    >>> under_30.count()
    207737

Text Ranges
-----------

Using the inequality operators with a **Text** variable
allows you to select values that are alphabetically earlier or later than a given value.

.. code-block:: python

    >>> second_half_of_alphabet = people["Surname"] >= "N"
    >>> second_half_of_alphabet.count()
    410954

Restrictions on using inequality operators
------------------------------------------

All of the examples above specify an *unbounded* range of values
— it is only limited by one value,
and allows all values above or below this (depending on the operator used).

.. warning::
    You **cannot** use two inequality operators at once,
    for example, to try to pick values bounded within a range on either side.
    So the following code **will not** have the desired effect:

    .. code-block:: python

        >>> born_in_1990 = date(1990, 1, 1) <= people["DOB"] <= date(1990, 12, 31)

    See the warning about :ref:`operator_chaining`
    in the variables reference guide for more information about this.

We will learn in the next part how to achieve the desired result
by joining more than one selection together instead.
