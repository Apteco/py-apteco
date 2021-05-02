.. _cube_reference:

********
  Cube
********

.. py:currentmodule:: apteco.cube


Introduction
============

The :class:`Cube` object corresponds to a FastStats Cube
and is a multi-dimensional numeric analysis of FastStats data.

The cube is specified by:

    * a resolve **table** – statistics on the cube are measures of
      records in this table
    * a set of **dimensions** – these are the fields over which the data
      is being analysed
    * a set of **measures** – these define the statistics displayed on the cube
      to analyse the data
    * a base **selection** *(optional)* – this filters records in the table
      to only include in the analysis ones that match the given criteria

.. note::
    Currently, the cube dimensions must be **Selector** variables
    or **banded Date** variables.
    Other variable types and more complex types like expressions or selections
    are not yet supported.

Basic use
=========

Setting up variables::

    >>> people = my_session.tables["People"]
    >>> occupation = people["Occupation"]
    >>> income = people["Income"]
    >>> gender = people["Gender"]

Creating a cube::

    >>> cube = people.cube([occupation, income, gender])

Converting to a Pandas :class:`DataFrame`::

    >>> df = cube.to_df()
    >>> df.head(10)
                                   People
    Occupation    Income  Gender
    Manual Worker <£10k   Female    15624
                          Male       5321
                          Unknown       5
                  £10-20k Female    43051
                          Male       5992
                          Unknown      25
                  £20-30k Female     1498
                          Male        649
                          Unknown      14
                  £30-40k Female      675

Pivoting the ``Occupation`` dimension to make it easier to read::

    >>> df.unstack(level=0)
                       People          ...
    Occupation       Director Manager  ... Student Unemployed
    Income   Gender                    ...
    <£10k    Female      1279    4649  ...   28002      21385
             Male         832    2926  ...   14296       8386
             Unknown        4      16  ...      10        155
    £10-20k  Female      4116   16665  ...   39462      17230
             Male        2139    9123  ...   17917       4532
             Unknown        9      47  ...      25        368
    £100k+   Female         2       1  ...       2          0
             Male           1       0  ...       3          0
             Unknown        1       0  ...       1          0
    £20-30k  Female      1267    6238  ...    6669       5747
             Male        1050    5315  ...    5274       1345
             Unknown        5      45  ...      22        236
    £30-40k  Female      1591    6621  ...    5690       3117
             Male        1940    9713  ...    6345       1049
             Unknown       46     140  ...      63        519
    £40-50k  Female       265     965  ...     587        262
             Male         518    1800  ...     943        115
             Unknown       22      58  ...      29        110
    £50-60k  Female       336     806  ...     425        277
             Male         607    1677  ...     692         69
             Unknown       47      88  ...      64         89
    £60-70k  Female        40     112  ...      54         58
             Male          96     220  ...      95          8
             Unknown       11      16  ...      17         17
    £70-80k  Female        44      96  ...      42         27
             Male         102     179  ...      63          5
             Unknown       12      22  ...      15          5
    £80-90k  Female        11      11  ...       3          0
             Male          14      13  ...      16          0
             Unknown        4       3  ...       5          0
    £90-100k Female         1       0  ...       1          1
             Male          11       7  ...       4          0
             Unknown        3       6  ...       9          0

    [33 rows x 10 columns]

Using banded Date variables as dimensions::

    >>> bookings = my_session.tables["Bookings"]
    >>> booking_date = bookings["Booking Date"]
    >>> travel_date = bookings["Travel Date"]
    >>> booking_travel_cube = bookings.cube([booking_date.month, travel_date.year])
    >>> booking_travel_df = booking_travel_cube.to_df()
    >>> booking_travel_df.unstack(level=1)
                         Bookings
    Travel Date (Year)       2016 2017 2018 2019 2020   2021   2022
    Booking Date (Month)
    2016-01                  2668    0    0    0    0      0      0
    2016-02                 24482    0    0    0    0      0      0
    2016-03                 28435    0    0    0    0      0      0
    2016-04                 24360    0    0    0    0      0      0
    2016-05                 22757    0    0    0    0      0      0
                           ...  ...  ...  ...  ...    ...    ...
    2021-08                     0    0    0    0    0  39880      0
    2021-09                     0    0    0    0    0  34380    407
    2021-10                     0    0    0    0    0  21537   6824
    2021-11                     0    0    0    0    0  12078  14308
    2021-12                     0    0    0    0    0   2938  16737

    [72 rows x 7 columns]

Using a base selection to filter the records::

    >>> student = occupation == "4"
    >>> student_cube = student.cube([occupation, income, gender])
    >>> student_df = student_cube.to_df()
    >>> student_df.head()
                                   People
    Occupation    Income  Gender
    Manual Worker <£10k   Female        0
                          Male          0
                          Unknown       0
                  £10-20k Female        0
                          Male          0

Selecting only cells where ``Occupation`` is *Student*,
and pivoting ``Gender`` dimension::

    >>> student_df.loc["Student"].unstack(level=1)
             People
    Gender   Female   Male Unknown
    Income
    <£10k     28002  14296      10
    £10-20k   39462  17917      25
    £100k+        2      3       1
    £20-30k    6669   5274      22
    £30-40k    5690   6345      63
    £40-50k     587    943      29
    £50-60k     425    692      64
    £60-70k      54     95      17
    £70-80k      42     63      15
    £80-90k       3     16       5
    £90-100k      1      4       9

Using a base selection from a different table::

    >>> households = my_session.tables["Households"]
    >>> region = households["hoRegion"]
    >>> manchester = region == "13"
    >>> manc_cube = manchester.cube([occupation, region, gender], table=people)
    >>> manc_df = manc_cube.to_df()
    >>> manc_df.loc["Manager"].unstack(level=1)
                                          People
    Gender                                Female  Male Unknown
    Region
    Channel Islands                            0     0       0
    East Anglia                                0     0       0
    East Midlands                              0     0       0
    Greater Manchester                      1554  1539      26
    North                                      0     0       0
    North West (Excluding Gtr Manchester)      0     0       0
    Northern Ireland                           0     0       0
    Scotland                                   0     0       0
    South East (Inside M25 )                   0     0       0
    South East (Outside M25 )                  0     0       0
    South West                                 0     0       0
    Wales                                      0     0       0
    West Midlands                              0     0       0
    Yorkshire and Humber                       0     0       0

Adding different measures::

    >>> from apteco.statistics import Sum, Mean
    >>> cost = bookings["Cost"]
    >>> profit = bookings["Profit"]
    >>> finance_cube = bookings.cube([dest, gender], measures=[Mean(cost), Sum(profit)])
    >>> finance_df = finance_cube.to_df()
    >>> finance_df.unstack(1)
                  Mean(Cost)                  Sum(Profit)
    Gender            Female    Male Unknown       Female         Male     Unknown
    Destination
    Australia         641.33  642.80  641.63   4969609.27   9289372.33   338911.11
    Denmark           636.56  552.11  673.20     77696.43      7172.64    11138.75
    France            644.34  645.12     NaN  28028207.53  12743135.05        0.00
    Germany           643.13  688.66  739.48  41693688.99     49751.52     2396.78
    Greece            644.01  643.99  652.30   3969380.08   7381942.89   259677.61
    Italy             638.27  634.36  658.72   3362435.25    502193.53   402007.87
    Jamaica           597.36  468.56  807.87      1770.04       290.77       15.51
    Kuwait            650.15  645.65  659.84    298712.85    554525.03    67014.61
    Latvia            693.92  618.84  712.12     11177.66     19882.72     2592.66
    Mali              596.55  661.02  771.80     18392.77     40416.47     4736.45
    Mongolia          579.34  636.74  677.02      4193.65      7141.89     2213.89
    Namibia           704.16  638.48  542.54     31981.71     57459.89     3439.89
    New Zealand       633.99  641.36  625.06     17982.15     33741.93     4577.55
    Portugal          636.00  650.95  647.02    890531.92    554791.39   229951.78
    Senegal           656.55  658.48  518.11     60939.12     28611.82      946.95
    Sierra Leone      614.09  652.47  597.09    165479.74    353473.04    33155.92
    South Africa      682.05  694.72  748.89     41997.60     84264.98     6911.85
    Sweden            641.35  644.49  652.47   1232007.22   2296749.68    57618.93
    United States     638.56  640.62  632.76  25279636.01  46492373.17  7632493.15

.. Cube-related tasks
.. ==================

API reference
=============

Cube creation and conversion
----------------------------

.. class:: Cube(dimensions, measures=None, selection=None, table=None, *, session=None)

    Create a cube.

    .. tip::
        The :meth:`cube` methods on tables and selections are wrappers
        around this class.
        It is recommended to prefer those over instantiating this class directly,
        as they generally provide a simpler interface.

    :param list[Variable] dimensions: Variables to use as dimensions in the cube.
        These must be from `table` or from a 'related' table
        – either an ancestor or descendant.
    :param list measures: Statistics to display in the cube.
        These must be from `table` or from a 'related' table
        – either an ancestor or descendant.
        If `measures` is None, the count measure of the cube's resolve table
        will be used by default.
    :param Clause selection: Optional base selection to apply to the cube.
        The table of this selection must be a 'related' table
        – either an ancestor or descendant.
    :param Table table: Resolve table of the cube.
        This table's records are used in the analysis for the cube,
        e.g. the default count measure is a count of records from this table.
    :param Session session: Current Apteco API session.

    As well as being related to `table`,
    the following restrictions apply to dimensions and measures:

        * All dimensions must be from tables related to each other,
          except in the case of a 'cross cube'
          when dimensions may be from unrelated tables,
          as long as these are all descendants of `table`.
        * Each measure's table must be related to each dimension's table.
          In the case of a 'cross cube', all measures must be from `table`
          or one of its ancestors.

    At least one of `selection` or `table` must be given:

        * If only `selection` is given,
          then `table` will be set to the resolve table of the selection.
        * If both are given and the resolve table of `selection`
          isn't `table`,
          then the records used in the cube
          are determined by mapping the selection to the required table by applying
          **ANY**/**THE** logic as necessary.
          This matches the behaviour when applying an underlying selection
          to a cube in the FastStats application.
          The mapping described here happens in the FastStats data engine
          and does not change the `selection` on the :class:`Cube`.

    .. tip::
        The following two cubes are equivalent::

            >>> cube1 = Cube(
            ...     dimensions,
            ...     selection=manchester,
            ...     table=people,
            ...     session=my_session,
            ... )
            >>> cube2 = Cube(
            ...     dimensions,
            ...     selection=(people * manchester),
            ...     session=my_session,
            ... )

        They both return a cube counting *people*
        from households in the Greater Manchester region.

    .. note::
        The raw cube data is fetched from the Apteco API
        when the :class:`Cube` object is initialised.
        It is held on the object in the :attr:`_data` attribute as a Numpy :class:`array`
        but this is not considered public, and so to work with the data
        you should convert it to your desired output format.
        The format currently supported is a Pandas :class:`DataFrame`,
        via the :meth:`to_df` method.

    .. method:: to_df(unclassified=False, totals=False, no_trans=False, convert_index=True)

        Return the cube as a Pandas :class:`DataFrame`.
        This is configured such that:

            * the dimensions form the **index**.
              If multiple dimensions are given, this is a :class:`MultiIndex`
              with each level corresponding to a dimension.
            * there is one **column** for each measure.

        :param bool unclassified: Whether to include unclassified rows in the DataFrame.
            Default is `False`.
        :param bool totals: Whether to include totals rows in the DataFrame.
            Default is `False`.
        :param bool no_trans: Whether to include rows counting records
            with no transactions;
            applicable when at least one dimension belongs to a child table.
            *Included for forwards-compatibility, but not currently implemented.*
            *Must be left as False.*
        :param bool convert_index: Whether to convert the index to the corresponding
            'natural' Pandas index type,
            or leave as a plain :class:`Index` with strings as labels.
            Conversion isn't possible if `unclassified` or `totals` is `True`.
            Default behaviour is to convert if possible.

        .. tip::
            The structure of the DataFrame returned by the :meth:`to_df()` method
            is very similar to a *Tree* in the FastStats application.

        .. seealso::
            For more details on working with a Pandas DataFrame
            with a MultiIndex,
            see the `user guide
            <https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html>`_
            in the official Pandas documentation.

Dimensions
----------

This section lists the various objects that can be applied as dimensions on a cube.
It also details their behaviour when the cube is transformed into a pandas DataFrame
under the :meth:`to_df()` method.

Selector variables
~~~~~~~~~~~~~~~~~~

Selector variables can be used directly as cube dimensions,
though this doesn't include any selector sub-types,
such as Array or Flag Array variables.
(The exception to this is Date and DateTime variables,
which can be used as dimensions when a banding is applied – see the section below.)

Conversion to a pandas DataFrame:

* The index is left as a standard pandas :class:`Index`.
* The index labels are the dimension category descriptions.
* The index name is the variable description.

Banded Date variables
~~~~~~~~~~~~~~~~~~~~~

Date and DateTime variables can be used as cube dimensions
when banded up to a particular time period.
These bandings are accessed via attributes on the :class:`DateVariable`
or :class:`DateTimeVariable` object.

The following bandings are currently supported:

* ``DateVariable.day``
* ``DateVariable.month``
* ``DateVariable.quarter``
* ``DateVariable.year``

Conversion to a pandas DataFrame:

* The default index conversion is to a pandas :class:`PeriodIndex`
  with the corresponding frequency (see table below).
* If not converted, the index labels are datetime strings (see table table below).
* The index name is of the form `'<Variable description> (<banding>)'`.

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Banding
     - `Date Offset <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects>`_
     - Frequency string
     - Examples (unconverted string labels)
   * - ``day``
     - Day
     - ``'D'``
     - ``'2019-01-01'`` ``'2019-01-02'`` ``'2019-01-03'``
   * - ``month``
     - Month
     - ``'M'``
     - ``'2019-01'`` ``'2019-02'`` ``'2019-03'``
   * - ``quarter``
     - Quarter
     - ``'Q'``
     - ``'2019-Q1'`` ``'2019-Q2'`` ``'2019-Q3'``
   * - ``year``
     - Year
     - ``'A'``
     - ``'2019'`` ``'2020'`` ``'2021'``

Statistics
----------

.. py:currentmodule:: apteco.statistics

Two types of statistics are currently supported as cube measures:
table counts and variable statistics.

Table counts
~~~~~~~~~~~~

These can be specified by passing a Table object in the `measures` list,
and will return a count of the records from that Table.
If `measures` is None, the count of records from the resolve table
will be used by default.

Variable statistics
~~~~~~~~~~~~~~~~~~~

These are summary statistics over a given variable and can be specified
using the classes available in the :mod:`apteco.statistics` module.

The statistics all have the same signature:

.. class:: Statistic(operand, *, label=None)

    Create a variable statistic.

    :param Variable operand: Variable over which to apply the statistic.
        Most statistics can only be calculated over numeric variables,
        but some also accept selector variables.
        See details below for specific restrictions.
    :type label: str, optional
    :param label: Descriptive name for this statistic.
        Used as the column label for this statistic
        on the DataFrame returned by :meth:`to_df`.

Selector or Numeric variable
""""""""""""""""""""""""""""

These statistics accept either a **selector** or **numeric** variable as the operand:


.. class:: CountMode

    The number of records which take the modal value of the variable.


.. class:: CountDistinct

    The number of distinct values of the variable.

Numeric variable
""""""""""""""""

These statistics accept a **numeric** variable as the operand:


.. class:: Sum

    The sum of values of the variable.


.. class:: Min

    The minimum value of the variable.


.. class:: Max

    The maximum value of the variable.

.. class:: Populated

    The number of records for which the variable has a (non-missing) value.

.. class:: Mode

    The mode (most common) value of the variable.


.. class:: Mean

    The mean value of the variable.


.. class:: StdDev

    The standard deviation of the variable.


.. class:: Variance

    The variance of the variable.


.. class:: Median

    The median value of the variable.


.. class:: LowerQuartile

    The lower quartile of the variable.


.. class:: UpperQuartile

    The upper quartile of the variable.


.. class:: InterQuartileRange

    The inter-quartile range of the variable.

