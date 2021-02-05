.. _variables_reference:

*************
  Variables
*************

Introduction
============

The :class:`Variable` object represents a FastStats system variable.
It holds metadata about the FastStats variable,
and has a reference to the :class:`Table` object
corresponding to the FastStats table the variable belongs to.
But its main use is in enabling you to build selections
in a quick and intuitive way.
:class:`Variable` objects for a FastStats system are automatically created
when you initialize a :class:`Session` connected to that system.

Basic use
=========

Retrieving a variable from a :class:`Session` object::

    >>> cost = my_session.variables["Cost"]

Retrieving a variable from its :class:`Table` object::

    >>> gender = people["Gender"]

Examining variable metadata::

    >>> print(
    ...     f"'{cost.description}' is a"
    ...     f"{' virtual' if cost.is_virtual else ''}"
    ...     f" {cost.type} variable on the '{cost.table_name}' table."
    ... )
    ...
    'Cost' is a Numeric variable on the 'Bookings' table.

Building a selection::

    >>> expensive_bookings = cost > 2000
    >>> expensive_bookings.count()
    53266

Variable-related tasks
======================

Retrieving a variable
---------------------

Variables can be accessed through the :attr:`variables` attribute
on a :class:`Session` object.
You can look up variables by their name or description::

    >>> surname = my_session.variables["peSName"]
    >>> income = my_session.variables["Income"]

Similarly, there is a :attr:`variables` attribute on each :class:`Table` object
for accessing the variables from that table.
However, for convenience it's possible to just index directly into
the :class:`Table` itself::

    >>> car_make_code = households["HHCarmak"]
    >>> profit = bookings["Profit"]

Building a selection
--------------------

Variable objects can be used as the starting point for creating selections.
Selections can be built up by specifying accepted values for a given variable
using the Python comparison operators::

    >>> destination = my_session.variables["Destination"]
    >>> bookings_to_sweden = destination == "29"
    >>> bookings_to_sweden.count()
    25207
    >>> profit = my_session.variables["Profit"]
    >>> high_value_bookings = profit > 500
    >>> high_value_bookings.count()
    14428

For details on variable types, their supported operators and accepted values,
see the variables :ref:`variable_api_reference` section below.

.. _variable_api_reference:

API reference
=============

General variable properties
---------------------------

.. class:: Variable

    The base class for all variables.
    It has various attributes for variable metadata common to all variable types.

    .. py:attribute:: name

        The variable's short reference name (e.g. `boDest`).

    .. py:attribute:: description

        The variable's descriptive name (e.g. `Destination`).

    .. py:attribute:: type

        A string of the variable's type.

    .. py:attribute:: folder_name

        The FastStats system folder this variable belongs to.

    .. py:attribute:: table

        The table this variable is from (a :class:`Table` object).

    .. py:attribute:: table_name

        The name of the table this variable is from
        (alias of :attr:`table.name`).

    .. py:attribute:: is_selectable

        Whether the variable is allowed to be used in selections.

    .. py:attribute:: is_browsable

        Whether the variable is allowed
        to be viewed with a client application (but not exported).

    .. py:attribute:: is_exportable

        Whether the variable is allowed
        to be exported by a client application.

    .. py:attribute:: is_virtual

        Whether the variable is a virtual variable.

Selector-type variables
-----------------------

.. class:: BaseSelectorVariable

    The base class for selector-type variables
    with attributes common to all of them.

    .. py:attribute:: code_length

        The length (in bytes) of the var codes for this variable.

    .. py:attribute:: num_codes

        The number of different var codes this variable has.

    .. py:attribute:: var_code_min_count

        The number of records that have the var code with the smallest count.

    .. py:attribute:: var_code_max_count

        The number of records that have the var code with the largest count.

    .. py:attribute:: var_code_order

        How the var codes are ordered for this variable, out of:
        **Nominal**, **Ascending**, **Descending**.

Selector variable
-----------------

.. class:: SelectorVariable

    Subclass of :class:`BaseSelectorVariable` which represents
    a standard FastStats **Selector** variable.

Operators
~~~~~~~~~

Use the equals operator ``==`` to select records
where this selector variable equals the given value.
If multiple values are given, it must be equal to one of them.

    >>> sweden = bookings["Destination"] == "29"
    >>> high_earners = people["Income"] == ["07", "08", "09", "10", "11"]

Use the 'not equals' operator ``!=`` to select records
where this selector variable does not equal the given value.
If multiple values are given, it must not be equal to any of them.

    >>> not_unclassified = people["Occupation"] != "!"
    >>> england = households["Region"] != ["10", "11", "12", "14"]


Numeric variable
----------------

.. class:: NumericVariable

    Class which represents a FastStats **Numeric** variable.

    .. py:attribute:: min_value

        The smallest value of this variable over all records.

    .. py:attribute:: max_value

        The largest value of this variable over all records.

    .. py:attribute:: is_currency

        Whether this variable represents a currency value.

    .. py:attribute:: currency_locale

        Locale name for the currency (if this is a currency variable).

    .. py:attribute:: currency_symbol

        Currency symbol for the currency (if this is a currency variable).

.. py:method:: NumericVariable.missing(*, include=True, label=None)

    Select records where this numeric variable's value is missing.

    :type label: str or None
    :param bool include: set to `False` to *exclude* missing values
        from the selection (default is `True`)
    :param label: textual label for this selection clause

Operators
~~~~~~~~~

Use the ``==`` operator to select records
where this numeric variable equals the given value.
If multiple values are given, it must be equal to one of them.

    >>> booked_3_days_ago = policies["Days Since Booking"] == 3
    >>> cost_multiple_of_100 = bookings["Cost"] == [i * 100 for i in range(1, 284)]

Use the ``!=`` operator to select records
where this numeric variable does not equal the given value.
If multiple values are given, it must not be equal to any of them.

    >>> some_profit = bookings["Profit"] != 0
    >>> waiting_more_than_week = journeys["Days Waiting"] != range(7)

Use the ``<=`` operator to select records
where this numeric variable is less than or equal to the given value.

    >>> premium_up_to_25 = policies["Premium"] <= 25

Use the ``>=`` operator to select records
where this numeric variable is greater than or equal to the given value.

    >>> high_profit = bookings["Profit"] >= 1000

Use the ``<`` operator to select records
where this numeric variable is strictly less than the given value.

    >>> visit_shorter_than_minute = web_visits["Duration"] < 60

Use the ``>`` operator to select records
where this numeric variable is strictly greater than the given value.

    >>> more_than_4_weeks_to_travel = policies["Days Until Travel"] > 28

.. warning::

    You **cannot** use two comparison operators at once,
    for example, to try to pick values bounded within a range on either side.
    So the following code **will not** have the desired effect:

    .. code-block:: python

        >>> cost_between_50_100 = 50 <= bookings["Cost"] <= 100

    See the :ref:`operator_chaining` section below for more details.

Text variable
-------------

.. py:attribute:: TextVariable.max_length

    An integer giving the maximum length (in bytes) of text data per record
    for this variable.

.. py:method:: TextVariable.equals(value, match_case=True, *, include=True, label=None)

    Select records where this text variable equals the given value.
    If multiple values are given, it must be equal to one of them.

    Can also use the ``==`` operator, or ``!=`` for `include=False`.

    :type value: str or Iterable[str]
    :type label: str or None
    :param value: value(s) to use in the selection
    :param bool match_case: set to `False` to perform case-insensitive
        matching on the given values (default is `True`)
    :param bool include: set to `False` to specify these as values
        to *exclude* from the selection (default is `True`)
    :param label: textual label for this selection clause

.. py:method:: TextVariable.contains(value, match_case=True, *, include=True, label=None)

    Select records where this text variable contains the given value.
    If multiple values are given, it must contain at least one of them.

    :type value: str or Iterable[str]
    :type label: str or None
    :param value: value(s) to use in the selection
    :param bool match_case: set to `False` to perform case-insensitive
        matching on the given values (default is `True`)
    :param bool include: set to `False` to specify these as values
        to *exclude* from the selection (default is `True`)
    :param label: textual label for this selection clause

.. py:method:: TextVariable.startswith(value, match_case=True, *, include=True, label=None)

    Select records where this text variable begins with the given value.
    If multiple values are given, it must begin with one of them.

    :type value: str or Iterable[str]
    :type label: str or None
    :param value: value(s) to use in the selection
    :param bool match_case: set to `False` to perform case-insensitive
        matching on the given values (default is `True`)
    :param bool include: set to `False` to specify these as values
        to *exclude* from the selection (default is `True`)
    :param label: textual label for this selection clause

.. py:method:: TextVariable.endswith(value, match_case=True, *, include=True, label=None)

    Select records where this text variable ends with the given value.
    If multiple values are given, it must end with one of them.

    :type value: str or Iterable[str]
    :type label: str or None
    :param value: value(s) to use in the selection
    :param bool match_case: set to `False` to perform case-insensitive
        matching on the given values (default is `True`)
    :param bool include: set to `False` to specify these as values
        to *exclude* from the selection (default is `True`)
    :param label: textual label for this selection clause

.. .. py:method:: before(self, value, allow_equal=False, *, include=True, label=None)
..
..     Select records where this text variable is alphabetically before
..     the given value. Set `allow_equal=True` to include the value itself.
..     This method is *not* case-sensitive.
..
..     Can also use the ``<`` operator or ``<=`` for `allow_equal=True`.
..
..     :type label: str or None
..     :param str value: value to use in the selection
..     :param bool allow_equal: set to `True` to include the value itself
..         (default is `False`)
..     :param bool include: set to `False` to specify these as values
..         to *exclude* from the selection (default is `True`)
..     :param label: textual label for this selection clause
..
.. .. py:method:: after(self, value, allow_equal=False, *, include=True, label=None)
..
..     Select records where this text variable is alphabetically after
..     the given value. Set `allow_equal=True` to include the value itself.
..     This method is *not* case-sensitive.
..
..     Can also use the ``>`` operator or ``>=`` for `allow_equal=True`.
..
..     :type label: str or None
..     :param str value: value to use in the selection
..     :param bool allow_equal: set to `True` to include the value itself
..         (default is `False`)
..     :param bool include: set to `False` to specify these as values
..         to *exclude* from the selection (default is `True`)
..     :param label: textual label for this selection clause

.. py:method:: TextVariable.between(start, end, *, include=True, label=None)

    Select records where this text variable is alphabetically
    between `start` and `end` (inclusive).
    This method is *not* case-sensitive.

    :type label: str or None
    :param str start: start of permitted range
    :param str end: end of permitted range
    :param bool include: set to `False` to specify these as values
        to *exclude* from the selection (default is `True`)
    :param label: textual label for this selection clause

.. py:method:: TextVariable.matches(value, match_case=True, *, include=True, label=None)

    Select records where this text variable matches the given value,
    based on wildcard matching rules.
    If multiple values are given, it must match at least one of them.

    :type value: str or Iterable[str]
    :type label: str or None
    :param value: value(s) to use in the selection
        (see below for details of wildcards)
    :param bool match_case: set to `False` to perform case-insensitive
        matching on the given values (default is `True`)
    :param bool include: set to `False` to specify these as values
        to *exclude* from the selection (default is `True`)
    :param label: textual label for this selection clause

    **Wildcards**

    .. list-table::
       :header-rows: 1
       :widths: auto

       * - Wildcard
         - Explanation
         - Examples
       * - ``?``
         - matches any single character
         - ``Sm?th`` matches ``Smith``, ``Smyth``
       * - ``*``
         - matches any number of characters, or none
         - ``Smith*`` matches ``Smith``, ``Smithers``, ``Smith-Wood``
       * - ``?``, ``*``
         - (the two wildcards can be used in conjunction)
         - ``Sm?th*`` matches all of the above, as well as ``Smethurst``, ``Smythe``

Operators
~~~~~~~~~

Use the equals operator ``==`` to select records
where this text variable equals the given value.
If multiple values are given, it must be equal to one of them.

    >>> smiths = people["Surname"] == "Smith"
    >>> royal = people["Surname"] == ["King", "Queen", "Prince", "Princess"]

Use the 'not equals' operator ``!=`` to select records
where this text variable does not equal the given value.
If multiple values are given, it must not be equal to any of them.

    >>> not_s = people["Initial"] != "S"
    >>> consonant = people["Initial"] != list("AEIOU")


Array variable
--------------

.. class:: ArrayVariable

    Subclass of :class:`BaseSelectorVariable` which represents
    a FastStats **Array** variable.

Operators
~~~~~~~~~

Use the equals operator ``==`` to select records
where this array variable has the given value.
If multiple values are given, it must have one of them.

    >>> james_bond = households["Car Make Code"] == "ASM"
    >>> french_car = households["Car Make Code"] == ["CIT", "PEU", "REN"]

Use the 'not equals' operator ``!=`` to select records
where this array variable does not have the given value.
If multiple values are given, it must not have any of them.

    >>> not_unclassified_car = households["Car Make Code"] != "  !"
    >>> not_f_car = households["Car Make Code"] != ["FER", "FIA", "FOR"]

Flag array variable
-------------------

.. class:: FlagArrayVariable

    Subclass of :class:`BaseSelectorVariable` which represents
    a FastStats **FlagArray** variable.

Operators
~~~~~~~~~

Use the equals operator ``==`` to select records
where this flag array variable has the given value.
If multiple values are given, it must have one of them.

    >>> financial_times_reader = people["Newspapers"] == "Financial Times"
    >>> tabloid_reader = people["Newspapers"] == [
    ...     "Daily Express", "The Sun", "Daily Mirror", "Daily Mail", "Record"
    ... ]

Use the 'not equals' operator ``!=`` to select records
where this flag array variable does not have the given value.
If multiple values are given, it must not have any of them.

    >>> self_catering = bookings["Facilities"] != "Food"
    >>> cannot_contact = people["Contact Permission"] != ["EPS", "MPS", "TPS", "FPS"]

Date-type variables
-------------------

.. class:: BaseDateVariable

    A subclass of :class:`BaseSelectorVariable`
    which is the base class for date-type variables,
    with attributes common to all of them.

    .. py:attribute:: min_date

        The earliest date value of this variable over all records.

    .. py:attribute:: max_date

        The latest date value of this variable over all records.

Date variable
-------------

.. class:: DateVariable

    Subclass of :class:`BaseDateVariable` which represents
    a FastStats **Date** variable.

Operators
~~~~~~~~~

Use the equals operator ``==`` to select records
where this date variable is the given date.
If multiple dates are given, it must be one of them.

    >>> from datetime import date
    >>> christmas_day_2018 = bookings["Booking Date"] == date(2018, 12, 25)
    >>> valentines_day = bookings["Travel Date"] == [
    ...     date(y, 2, 14) for y in range(2016, 2023)
    ... ]

Use the equals operator ``!=`` to select records
where this date variable is not the given date.
If multiple dates are given, it must not be any of them.

    >>> not_new_years_day_2020 = bookings["Travel Date"] != date(2020, 1, 1)
    >>> not_easter = bookings["Travel Date"] != [
    ...     date(2016, 3, 27)
    ...     date(2017, 4, 16)
    ...     date(2018, 4, 1)
    ...     date(2019, 4, 21)
    ...     date(2020, 4, 12)
    ...     date(2021, 4, 4)
    ...     date(2022, 4, 17)
    ... ]

Use the ``<=`` operator to select records
where this date variable is before the given date (or is the date itself).

    >>> bookings_before_2019 = bookings["Booking Date"] <= date(2018, 12, 31)

Use the ``>=`` operator to select records
where this date variable is after the given date (or is the date itself).

    >>> from dateutil.relativedelta import relativedelta
    >>> under_30 = people["DOB"] >= date.today() - relativedelta(years=30)

.. warning::

    You **cannot** use two comparison operators at once,
    for example, to try to pick values bounded within a range on either side.
    So the following code **will not** have the desired effect:

    .. code-block:: python

        >>> summer_holiday_2019 = date(2019, 7, 1) <= bookings["Travel Date"] <= date(2019, 8, 31)

    See the :ref:`operator_chaining` section below for more details.

Date-time variable
------------------

.. class:: DateTimeVariable

    Subclass of :class:`BaseDateVariable` which represents
    a FastStats **DateTime** variable.

Operators
~~~~~~~~~

Use the ``<=`` operator to select records
where this datetime variable is before the given datetime
(or is the datetime itself).

    >>> before_4pm_halloween_2019 = web_visits["wvTime"] <= datetime(
    ...     2019, 10, 31, 15, 59, 59
    ... )

Use the ``>=`` operator to select records
where this datetime variable is after the given datetime
(or is the datetime itself).

    >>> after_july_2016 = communications["cmCommDt"] >= datetime(2016, 8, 1, 0, 0, 0)

.. warning::

    You **cannot** use two comparison operators at once,
    for example, to try to pick values bounded within a range on either side.
    So the following code **will not** have the desired effect:

    .. code-block:: python

        >>> during_webinar = datetime(2019, 6, 3, 15) <= web_visits["wvTime"] <= datetime(2019, 6, 3, 16)

    See the :ref:`operator_chaining` section below for more details.

Reference variable
------------------

.. class:: ReferenceVariable

    Class which represents a FastStats **Reference** variable.

*(no operators are currently supported for* :class:`ReferenceVariable` *objects)*

.. _operator_chaining:

Operator chaining
-----------------

The following is true for all variable types,
as it also applies to the [not] equals operators ``==``, ``!=``,
but is particularly relevant for those types that support the operators
``<=``, ``>=``, ``<``, ``>``:
**Numeric**, **Date**, **DateTime**

.. warning::

    You **cannot** use two comparison operators at once,
    for example, to try to pick values bounded within a range on either side.
    So the following code **will not** have the desired effect:

    .. code-block:: python

        >>> born_in_1990 = date(1990, 1, 1) <= people["DOB"] <= date(1990, 12, 31)

    Python *does* normally support this 'operator chaining' syntax
    when `using the operators for standard comparison
    <https://realpython.com/python-operators-expressions/
    #compound-logical-expressions-and-short-circuit-evaluation>`_,
    but it doesn't work in our situation where the operators have been overloaded
    for creating selections.

    In this example, because of the way `operator chaining
    <https://realpython.com/python-operators-expressions/#chained-comparisons>`_
    and short-circuit evaluation work,
    this ends up being equivalent to just the right-hand part of the expression:

    .. code-block:: python

        >>> born_in_1990 = people["DOB"] <= date(1990, 12, 31)
