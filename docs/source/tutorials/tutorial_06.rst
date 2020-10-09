************************************
  Combining selections using logic
************************************

In this part of the tutorial we'll learn
how to build more complex selections by joining separate parts together,
and how to use various types of logic in the process.

Joining two selections together
===============================

So far we've only looked at selections with one condition based on a single variable,
but we can combine these to create selections with multiple conditions.

We simply use the Python `bitwise and` operator ``&``
to combine two parts into one selection:

.. code-block:: python

    >>> sweden = bookings["Destination"] == "29"
    >>> at_least_2k = bookings["Cost"] >= 2000
    >>> expensive_sweden = sweden & at_least_2k
    >>> expensive_sweden.count()
    632

This works just like the **AND** logic in a selection tree
in the FastStats application:
a record (in this case, a booking) must match both conditions to be selected.

In a similar way, you can use the `bitwise or` operator ``|``
to combine selections using **OR** logic:

.. code-block:: python

    >>> student = people["Occupation"] == "4"
    >>> under_21 = people["DOB"] >= date.today() - relativedelta(years=21)
    >>> eligible_for_discount = student | under_21
    >>> eligible_for_discount.count()
    188364

.. note::

    Be sure to use the ``&`` and ``|`` operators,
    i.e. the *ampersand* and *vertical bar* symbols.
    Using the ``and`` or ``or`` keywords will **not** work.

Returning to the :ref:`example from the previous part <operator_chaining_warning>`,
here's how we can create a selection with values in a range bounded on both sides:

.. code-block:: python

    >>> born_in_1990 = (
    ...     (people["DOB"] >= date(1990, 1, 1))
    ...     & (people["DOB"] <= date(1990, 12, 31))
    ... )

Negating a clause
=================

To exclude a selection from the final count,
you can use the `bitwise not` operator ``~`` to apply **NOT** logic to it:

.. code-block:: python

    >>> high_earners = people["Income"] == (f"{i:02}" for i in range(7, 12))
    >>> low_mid_earners = ~high_earners
    >>> low_mid_earners.count()
    1149439

Of course, we could have made the same selection
by just selecting the low-mid income codes directly
or by swapping the ``==`` operator for ``!=``.
But the ``~`` is particularly useful to apply to a selection made of more than one part,
rather than trying to reverse the overall logic by changing the individual parts:

.. code-block:: python

    >>> eligible_for_discount = student | under_21
    >>> pay_full_price = ~eligible_for_discount
    >>> pay_full_price.count()
    968189

.. note::

    Be sure to use ``~`` operator,
    i.e. the *tilde* symbol.
    Using the ``not`` keyword will **not** work.

Joining across different tables
================================

The previous examples joined a pair of clauses from the *same* table,
but you can also combine clauses from *different* tables:

.. code-block:: python

    >>> high_earners = people["Income"] == (f"{i:02}" for i in range(7, 12))  # people selection
    >>> at_least_2k = bookings["Cost"] >= 2000  # bookings selection
    >>> high_affordability = high_earners | at_least_2k  # will resolve to people
    >>> high_affordability.count()
    56096
    >>> high_affordability.table_name
    'People'

When combining clauses from different tables
the resolve table of the resulting selection is determined by the **left-most** part.
In this example, that's the ``high_earners`` selection,
which is on the **People** table.

**py-apteco** automatically adapts other parts of the selection to match this,
by inserting the required table changes
using the **ANY** or **THE** operations familiar from FastStats selection trees.
So the selection in this example comprises 56,096 *people* who:

    * either have income of £60k+
    * or have made ANY *booking* costing at least £2k

Although the automatic table changes are often what we want,
we are also able to manually change the resolve table of a selection,
which we'll learn about in the next part.
