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

    >>> gender = people.variables["Gender"]

Examining variable metadata::

    >>> print(
            f"'{cost.description}' is a",
            f"{'virtual' if cost.is_virtual else ''}",
            f"{cost.type} variable on the '{cost.table.name}' table.",
        )
    'Cost' is a  Numeric variable on the 'Bookings' table.

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
This is a :class:`dict` where variables can be looked up by their description::

    >>> income = my_session.variables["Income"]

Similarly, there is a :attr:`variables` attribute on each :class:`Table` object
with just the variables for that table::

    >>> region = households.variables["Region"]

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

*(no extra properties beyond the common ones)*

Numeric variable
----------------

    * :attr:`min` (:class:`int` or :class:`float`): smallest value of this variable
      over all records
    * :attr:`max` (:class:`int` or :class:`float`): largest value of this variable
      over all records
    * :attr:`is_currency` (:class:`bool`): whether this variable represents
      a currency value
    * :attr:`currency_locale` (:class:`str`): locale name for the currency
      (if this is a currency variable)
    * :attr:`currency_symbol` (:class:`str`): currency symbol for the currency
      (if this is a currency variable)

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

Array variable
--------------

*(no extra properties beyond the common ones)*

Flag array variable
-------------------

*(no extra properties beyond the common ones)*

Date-type variables
-------------------

    * :attr:`min_date` (:class:`datetime.datetime`): earliest date value
      of this variable over all records
    * :attr:`max_date` (:class:`datetime.datetime`): latest date value
      of this variable over all records

Date-time variable
------------------

*(no extra properties beyond the common ones)*

Reference variable
------------------

*(no extra properties beyond the common ones)*
