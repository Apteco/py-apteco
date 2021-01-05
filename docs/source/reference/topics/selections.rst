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
    >>> sweden_dg = sweden.datagrid([urn, dest, trav, cost])
    >>> sweden_df = sweden_dg.to_df()
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
                            Bookings              ...
    Product       Accommodation Only Flight Only  ...  TOTAL Unclassified
    Destination                                   ...
    Australia                      0           0  ...      0            0
    Denmark                        0           0  ...      0            0
    France                         0           0  ...      0            0
    Germany                        0           0  ...      0            0
    Greece                         0           0  ...      0            0
    Italy                          0           0  ...      0            0
    Jamaica                        0           0  ...      0            0
    Kuwait                         0           0  ...      0            0
    Latvia                         0           0  ...      0            0
    Mali                           0           0  ...      0            0
    Mongolia                       0           0  ...      0            0
    Namibia                        0           0  ...      0            0
    New Zealand                    0           0  ...      0            0
    Portugal                       0           0  ...      0            0
    Senegal                        0           0  ...      0            0
    Sierra Leone                   0           0  ...      0            0
    South Africa                   0           0  ...      0            0
    Sweden                       277        2264  ...  25207            0
    TOTAL                        277        2264  ...  25207            0
    Unclassified                   0           0  ...      0            0
    United States                  0           0  ...      0            0

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

.. py:method:: sample(n=None, frac=None, sample_type="First", skip_first=0, *, label=None)
    Take a sample of records from the selection.

    :param int n: number of records to sample
        (cannot be used with `frac`)
    :param float frac: proportion of records to sample from the whole selection
        (cannot be used with `n`)
    :param str sample_type: type of sampling to use,
        one of: `First`, `Stratified`, `Random` (default is `Random`)
    :param int skip_first: number of records to skip from start of selection
        (default is `0`)
    :param str label: optional textual name for this selection clause
        (default is `None`)

.. py:method:: limit(n=None, frac=None, by=None, ascending=None, per=None, *, label=None)
    Limit the selection to a subset of records.

    :type ascending: bool or None
    :type per: Table or Variable
    :param int n: number of records to limit selection to
        (cannot be used with `frac`)
    :param float frac: proportion of records to limit selection to,
        out of whole selection (cannot be used with `n`)
    :param Variable by: variable to sort records by before limiting
        (if this is given and `ascending` isn't, default behaviour is to sort descending)
    :param ascending: whether to sort records ascending (`True`)
        or descending (`False`) before applying limit
        (if `by` is given and this isn't set, default behaviour is to sort descending)
    :param per:
        * **Table:** select `n` records per record on this parent table
        * **Variable:** select `n` records per value of this variable

Data Grids and Cubes
--------------------

.. py:method:: datagrid(columns, table=None, max_rows=1000)

    Build a data grid with this selection underlying it.

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

.. py:method:: cube(dimensions, measures=None, table=None)

    Build a cube with this selection underlying it.

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
