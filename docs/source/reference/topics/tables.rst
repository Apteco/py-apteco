.. _tables_reference:

**********
  Tables
**********

Introduction
============

The :class:`Table` object represents a FastStats system table.
It holds metadata about the FastStats table,
and provides access to all its variables.
It can also be used to help specify what records are included
in a selection, data grid or cube.
Table objects for a FastStats system are automatically created
when you initialize a :class:`Session` connected to that system.

Basic use
=========

Retrieving a table from a :class:`Session` object::

    >>> bookings = my_session.tables["Bookings"]

Examining table metadata::

    >>> print(
    ...     f"There are {bookings.total_records:,} {bookings.plural.lower()}"
    ...     f" in this system."
    ... )
    ...
    There are 2,130,081 bookings in this system.

Accessing variables::

    >>> cost = bookings["Cost"]
    >>> len(bookings.variables)
    14

Checking table relationships::

    >>> households = my_session.tables["Households"]
    >>> households.is_ancestor(bookings)
    True

Table-related tasks
===================

Changing the resolve table of a selection
-----------------------------------------

Using the ``*`` operator with a table object and a selection
enables you to change the resolve table of the selection::

    >>> people = my_session.tables["People"]
    >>> usa = bookings["Destination"] == "38"
    >>> been_to_usa = people * usa
    >>> been_to_usa.table_name
    'People'

Building a data grid or cube
----------------------------

Table objects can be used as the starting point
for creating a data grid using records from that table::

    >>> cols = (
            [people[var] for var in ("peInit", "peSName")]
            + [bookings[var] for var in ("boDate", "boCost", "boDest")]
        )
    >>> northern = households["Region"] == ["01", "02", "13"]
    >>> dg = bookings.datagrid(cols, northern, max_rows=100)
    >>> dg.to_df().head()
      Initial   Surname Booking Date     Cost    Destination
    0       A     Allen   2020-08-11   551.81         France
    1       W   Livesey   2021-08-02  1167.57   Sierra Leone
    2       W   Livesey   2021-08-19   562.56  United States
    3       W   Livesey   2021-08-08   960.55      Australia
    4       O  Robinson   2021-08-22   455.60  United States

You can similarly create a cube::

    >>> cube = bookings.cube(
            [people["Occupation"], bookings["Product"]],
            selection=(bookings["Cost"] > 200),
        )
    >>> df = cube.to_df().head(8)
                                      Bookings
    Occupation    Product
    Unclassified  Unclassified               0
                  Accommodation Only       109
                  Package Holiday         1840
                  Flight Only              566
                  TOTAL                   2515
    Manual Worker Unclassified               0
                  Accommodation Only      4039
                  Package Holiday        77547

API Reference
=============

General table properties & metadata
-----------------------------------

These attributes on the :class:`Table` object

.. py:attribute:: Table.name
    :type: str

    table reference name

.. py:attribute:: Table.singular
    :type: str

    noun for a single item from this table

.. py:attribute:: Table.plural
    :type: str

    noun for multiple items from this table

.. py:attribute:: Table.is_default
    :type: bool

    whether this is the default table for this FastStats system

.. py:attribute:: Table.is_people
    :type: bool

    whether this is the table representing people in this FastStats system

.. py:attribute:: Table.total_records
    :type: int

    total number of records on this table


Relationships with other tables
-------------------------------

These attributes on the :class:`Table` object hold data
about this table's related tables.
'Related' tables in this context covers:
**parent**, **children**, **ancestors** (this includes the parent),
**descendants** (this includes children).

.. py:attribute:: Table.child_relationship
    :type: str

    phrase to relate to this table from its parent,
    e.g. 'customer *<purchased the>* product'

.. py:attribute:: Table.parent_relationship
    :type: str

    phrase to relate this table to its parent,
    e.g. 'product *<was purchased by the>* customer'

.. py:attribute:: Table.has_children
    :type: bool

    whether this table has any child tables

.. py:attribute:: Table.parent_name
    :type: str

    name of this table's parent table (an empty string for the master table)

.. py:attribute:: Table.parent
    :type: Table

    the parent table of this table (:const:`None` for the master table)

.. py:attribute:: Table.children
    :type: list[Table]

    list of child tables of this table (an empty list if table has no children)

.. py:attribute:: Table.ancestors
    :type: list[Table]

    list of ancestor tables of this table (an empty list for the master table)

.. py:attribute:: Table.descendants
    :type: list[Table]

    list of descendant tables of this table (an empty list if table has no children)

Table comparison methods
------------------------

These methods on the :class:`Table` object enable you to compare it
with another table to check how they are related, if at all.

.. py:method:: Table.is_same(other)

    Return whether this table is the same as `other`.

    This comparison can also be performed using the ``==`` operator.

.. py:method:: Table.is_ancestor(other, allow_same=False)

    Return whether this table is an ancestor of `other`
    (the direct parent table also counts as an ancestor).
    If `allow_same` is set to `True`,
    this will also return `True` if the tables are the same.

    This comparison can also be performed using the ``<`` operator,
    or ``<=`` for `allow_same=True`.

.. py:method:: Table.is_descendant(other, allow_same=False)

    Return whether this table is a descendant of `other`
    (direct child tables also count as descendants).
    If `allow_same` is set to `True`,
    this will also return `True` if the tables are the same.

    This comparison can also be performed using the ``>`` operator,
    or ``>=`` for `allow_same=True`.

.. py:method:: Table.is_related(other, allow_same=False)

    Return whether this table is either an ancestor or descendant
    of `other`.
    If `allow_same` is set to `True`,
    this will also return `True` if the tables are the same.

    .. note::
        In one sense, all the tables in a FastStats system are related,
        since they are all descended from a single master table.
        However, 'related' here is referring to direct ancestor
        or direct descendant relationships,
        not including indirect 'sibling' or 'cousin' relationships.


Table variables
---------------

The variables on the table can be accessed through the
:attr:`variables` attribute.
This single object provides both a list-like and dictionary-like
interface for accessing variables.

Variables can be retrieved by indexing into this object
(using the ``[]`` operator)
with either the variable name or description::

    >>> cost = bookings.variables["Cost"]
    >>> destination = bookings.variables["boDest"]

This will raise a :exc:`KeyError` if the string you pass in
doesn't match a variable name or description.

There is also a shortcut for this by using the ``[]`` operator
directly on the table itself::

    >>> cost = bookings["Cost"]
    >>> destination = bookings["boDest"]

You can be explicit about picking by name or description
by using the :attr:`names` or :attr:`descs` attribute
on :attr:`variables`::

    >>> travel_date = bookings.variables.names["boTrav"]
    >>> profit = bookings.variables.descs["Profit"]

This will similarly raise a :exc:`KeyError`
if the lookup string is not recognised.
This includes if you pass a valid variable description
to :attr:`variables.names` and vice-versa.

The built-in :func:`len` function will give
the number of variables on the table::

    >>> len(bookings.variables)
    14

You can iterate over the variables::

    >>> for var in bookings.variables:
    ...     if var.type == "Numeric":
    ...         print(var.description)
    ...
    Cost
    Profit

You can also iterate over the variable names or descriptions::

    >>> [n for n in bookings.variables.names if not n.startswith("bo")]
    ['deType', 'deGrade', 'deMgr', 'deFacil']
    >>> [d for d in bookings.variables.descs if "date" in d.lower()]
    ['Booking Date', 'Travel Date', 'Busy dates']

.. note::
    Iterating over :attr:`variables` returns the :class:`Variable`
    objects, whereas iterating over :attr:`names` or :attr:`descs`
    returns the names or descriptions as strings.

.. seealso::
    Refer to the :ref:`variables_reference` documentation for more details
    on using variable objects.

Data Grids and Cubes
--------------------

.. py:method:: datagrid(columns, selection=None, max_rows=1000)

    Build a data grid with this table as the resolve table.

    >>> cols = (
            [people[var] for var in ("Initial", "Surname")]
            + [bookings[var] for var in ("boDate", "boCost", "boDest")]
        )
    >>> northern = households["Region"] == ["01", "02", "13"]
    >>> dg = bookings.datagrid(cols, northern, max_rows=100)
    >>> dg.to_df().head()
      Initial   Surname Booking Date     Cost    Destination
    0       A     Allen   2020-08-11   551.81         France
    1       W   Livesey   2021-08-02  1167.57   Sierra Leone
    2       W   Livesey   2021-08-19   562.56  United States
    3       W   Livesey   2021-08-08   960.55      Australia
    4       O  Robinson   2021-08-22   455.60  United States

    .. seealso::
        This method is a wrapper around the :class:`DataGrid` class.
        Refer to the :ref:`datagrid_reference` documentation for more details.

.. py:method:: cube(dimensions, measures=None, selection=None)

    Build a cube with this table as the resolve table.

    >>> cube = bookings.cube(
            [people["Occupation"], bookings["Product"]],
            selection=(bookings["Cost"] > 200),
        )
    >>> df = cube.to_df()
    >>> (
            df
            .drop("Unclassified", level=1)
            .unstack()
            .rename(columns=lambda x: x.split(" ")[0])
        )
                         Bookings
    Product         Accommodation  Package  Flight    TOTAL
    Occupation
    Director                 1714    24585    8477    34776
    Manager                  4422   109725   28566   142713
    Manual Worker            4039    77547   27104   108690
    Professional             1806    40072    9728    51606
    Public Sector           18308   249637   82437   350382
    Retail Worker            9864   126350   30853   167067
    Retired                 12750    86594   47333   146677
    Sales Executive         35214   407288  152911   595413
    Student                  6553   145156   27665   179374
    TOTAL                  103778  1326005  446288  1876071
    Unclassified              109     1840     566     2515
    Unemployed               8999    57211   30648    96858

    .. seealso::
        This method is a wrapper around the :class:`Cube` class.
        Refer to the :ref:`cube_reference` documentation for more details.
