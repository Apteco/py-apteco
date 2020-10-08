******************************
  Creating simple selections
******************************

In this part of the tutorial we'll learn
how to create and count simple selections,
involving one variable and a chosen value or set of values.

Making a simple selection
=========================

Selections can be built using :class:`Variable` objects
with the Python equality operator ``==`` to specify chosen values:

.. code-block:: python

    >>> sweden = bookings["boDest"] == "29"

Normally, the ``==`` operator would `test for equality
<https://docs.python.org/3/library/stdtypes.html#comparisons>`_
and return either :const:`True` or :const:`False`.
However, in **py-apteco** it is a shortcut for creating a selection:

.. code-block:: python

    >>> type(sweden)
    <class 'apteco.query.SelectorClause'>

You can then get a count of the selection by calling the :meth:`count` method on it:

.. code-block:: python

    >>> sweden.count()
    25207

Because the **Destination** variable is on the **Bookings** table,
this is a count of bookings.
We'll learn later on how to control which table we count.

.. tip::
    Make sure you use the different ``=`` symbols correctly:
    use the ``==`` comparison operator with the FastStats variable and chosen value(s)
    to create the selection,
    and the single ``=`` to assign the result of this to a Python variable.

Specifying multiple values
==========================

You can specify multiple values by using a list:

.. code-block:: python

    >>> fr_or_de_bookings = bookings["boDest"] == ["06", "07"]
    >>> fr_or_de_bookings.count()
    985734

In fact, you can use any Python `iterable`, except for a string
(which will be treated as a single value).
Here is an example using a generator expression:

.. code-block:: python

    >>> people = my_session.tables["People"]
    >>> high_earners = people["peIncome"] == (f"{i:02}" for i in range(7, 12))
    >>> high_earners.values
    ['07', '08', '09', '10', '11']
    >>> high_earners.count()
    7114

The format string ``f"{i:02}"`` left-pads the number ``i`` with ``0``\ s to a width of 2,
which matches the format of the **Income** selector codes.

As shown in these examples, when specifying values for **Selector** variables
you need to use selector codes given as strings (Python :class:`str` type variables).
In the next part, we'll learn about the different values we can give
for other FastStats variable types.
