**************
  Selections
**************

Introduction
============

A FastStats Selection is represented in **py-apteco** by a :class:`Clause` object,
possibly containing other nested or connected :class:`Clause` objects,
which combine to make the rule defining a set of records to be selected.
The table from which to select the records is also embedded in the rule.

As well as the fundamental action of counting a selection
to see how many records in the table match the conditions defined by the rule,
selections form the basis of many other pieces of analysis
and can be used in many different contexts.

Basic use
=========

Setting up variables::

    >>> from datetime import date
    >>> dest = bookings["Destination"]
    >>> trav = bookings["Travel Date"]
    >>> cost = bookings["Cost"]

Creating a selection::

    >>> sweden = dest == "29"
    >>> at_least_2k = cost >= 2000
    >>> before_2020 = trav <= date(2019, 12, 31)

Counting a selection::

    >>> sweden.count()
    25207

Combining selections::

    >>> sweden_before_2020 = sweden & before_2020
    >>> sweden_or_expensive = sweden | at_least_2k

Changing table::

    >>> been_to_sweden = people * sweden

Taking sample::

    >>> random_3_pct_sweden = sweden.sample(frac=0.03, sample_type="Random")

Applying limit::

    >>> top_1000_sweden_by_cost = sweden.limit(1000, by=cost)

Selection-related tasks
=======================

Building a data grid or cube
----------------------------

Selections can be used as the starting point
for creating a data grid using records in that selection::

    >>> urn = bookings["Booking URN"]
    >>> sweden_datagrid = sweden.datagrid([urn, dest, trav, cost])
    >>> sweden_df = sweden_datagrid.to_df()
    >>> sweden_df.head()
      Booking URN Destination Travel Date     Cost
    0    10172319      Sweden  2020-05-15  1201.81
    1    10384970      Sweden  2018-04-05   344.30
    2    10421011      Sweden  2019-07-11   322.89
    3    10425298      Sweden  2020-10-10   880.02
    4    10479109      Sweden  2020-09-21   172.91

You can similarly create a cube::

    >>> product = bookings["Product"]
    >>> grade = bookings["Grade"]
    >>> sweden_cube = sweden.cube([grade, dest, product])
    >>> sweden_df = sweden_cube.to_df()
    >>> sweden_df.loc["Silver"].unstack(level=1)
                            Bookings
    Product       Accommodation Only Flight Only Package Holiday
    Destination
    Australia                      0           0               0
    Denmark                        0           0               0
    France                         0           0               0
    Germany                        0           0               0
    Greece                         0           0               0
    Italy                          0           0               0
    Jamaica                        0           0               0
    Kuwait                         0           0               0
    Latvia                         0           0               0
    Mali                           0           0               0
    Mongolia                       0           0               0
    Namibia                        0           0               0
    New Zealand                    0           0               0
    Portugal                       0           0               0
    Senegal                        0           0               0
    Sierra Leone                   0           0               0
    South Africa                   0           0               0
    Sweden                       277        2264           22666
    United States                  0           0               0

API Reference
=============

Core attributes & methods
-------------------------

.. py:attribute:: table
    :type: Table

    resolve table of this selection

.. py:attribute:: table_name
    :type: str

    name of the resolve table of this selection

.. py:method:: count()

    return the number of records in this selection

Sampling and limits
-------------------

.. py:method:: sample(n=None, frac=None, sample_type="Random", skip_first=0, *, label=None)

    Take a sample of records from the selection.

    :param int n: Number of records to return from selection.
        Cannot be used with `frac`.
    :param float frac: Proportion of records to return out of whole selection,
        given as a number between 0 and 1.
        Cannot be used with `n`.
    :type sample_type: {'Random', 'Stratified', 'First'}
    :param sample_type: Type of sampling to use. Default is 'Random'.
    :param int skip_first: Number of records to skip from start of selection.
        Default is 0.
    :param str label: Optional textual name for this selection clause.

.. py:method:: limit(n=None, frac=None, by=None, ascending=None, per=None, *, label=None)

    Limit the selection to a subset of records.

    :type n: int or tuple
    :type frac: float or tuple
    :type ascending: bool, optional
    :type per: Table or Variable
    :param n: Number of records to return from selection.
        Cannot be used with `frac`.
        If `by` is given, a tuple of two integers `(i, j)` may be passed to
        select from the `i`\ th to the `j`\ th records.
    :param frac: Proportion of records to return out of whole selection,
        given as a number between 0 and 1.
        Cannot be used with `n`.
        If `by` is given, a tuple of two numbers `(p, q)` may be passed to
        select the proportion of records between them.
        For example `frac=(0.1, 0.25)` with `ascending=False`
        would give the top 10–25% of records.
    :param Variable by: Variable specifying order in which records are selected.
    :param ascending: Whether to order records ascending (`True`)
        or descending (`False`) when selecting limit.
        Must be used with `by`. Default is `False`.
    :param per: Return `n` records per this entity. Cannot be used with `frac`.
        If `per` is a **Table**, it must be a parent or ancestor table of the
        selection's table, and for each record on this table
        `n` child records are returned from the selection.
        If per is a **Variable**, `n` records are returned
        for each value of this variable.
        If `per` is a selector variable, this means `n` records
        for each selector category.
    :param str label: Optional textual name for this selection clause.

Data Grids and Cubes
--------------------

.. py:method:: datagrid(columns, table=None, max_rows=1000)

    Build a data grid with this selection underlying it.

    >>> cols = (
            [people[var] for var in ("Initial", "Surname")]
            + [bookings[var] for var in ("boDate", "boCost", "boDest")]
        )
    >>> northern = households["Region"] == ["01", "02", "13"]
    >>> datagrid = bookings.datagrid(cols, northern, max_rows=100)
    >>> datagrid.to_df().head()
      Initial   Surname Booking Date     Cost    Destination
    0       A     Allen   2020-08-11   551.81         France
    1       W   Livesey   2021-08-02  1167.57   Sierra Leone
    2       W   Livesey   2021-08-19   562.56  United States
    3       W   Livesey   2021-08-08   960.55      Australia
    4       O  Robinson   2021-08-22   455.60  United States

    .. seealso::
        This method is a wrapper around the :class:`DataGrid` class.
        Refer to the :ref:`datagrid_reference` documentation for more details.

.. py:method:: cube(dimensions, measures=None, table=None)

    Build a cube with this selection underlying it.

    >>> cube = bookings.cube(
            [people["Occupation"], bookings["Product"]],
            selection=(bookings["Cost"] > 200),
        )
    >>> df = cube.to_df()
    >>> df.unstack().rename(columns=lambda x: x.split(" ")[0])
                        Bookings
    Product         Accommodation  Flight Package
    Occupation
    Director                 1714    8477   24585
    Manager                  4422   28566  109725
    Manual Worker            4039   27104   77547
    Professional             1806    9728   40072
    Public Sector           18308   82437  249637
    Retail Worker            9864   30853  126350
    Retired                 12750   47333   86594
    Sales Executive         35214  152911  407288
    Student                  6553   27665  145156
    Unemployed               8999   30648   57211

    .. seealso::
        This method is a wrapper around the :class:`Cube` class.
        Refer to the :ref:`cube_reference` documentation for more details.
