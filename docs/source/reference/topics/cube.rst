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

    * a resolve **table** – statistics in the cube are measures of
      records in this table
    * a set of **dimensions** – these are the fields over which the data
      is being analysed
    * a set of **measures** – these define the statistics displayed in the cube
      to analyse the data
    * a base **selection** *(optional)* – this filters records in the table
      to only include in the analysis ones that match the given criteria

.. note::
    Currently, the cube dimensions must be FastStats **Selector** variables
    or **banded Date** variables.
    Other variable types and more complex types like expressions or selections
    are not yet supported.

Basic use
=========

Setting up variables::

    >>> bookings = my_session.tables["Bookings"]
    >>> dest = bookings["Destination"]
    >>> product = bookings["Product"]
    >>> grade = bookings["Grade"]

Creating a cube::

    >>> cube = bookings.cube([dest, product, grade])

Converting to a Pandas :class:`DataFrame`::

    >>> df = cube.to_df()
    >>> df.head(10)
                                           Bookings
    Destination Product            Grade
    Australia   Accommodation Only Gold           0
                                   Silver         0
                                   Bronze     10721
                Package Holiday    Gold           0
                                   Silver         0
                                   Bronze    134115
                Flight Only        Gold           0
                                   Silver         0
                                   Bronze    137883
    New Zealand Accommodation Only Gold           0

Pivoting the ``Destination`` dimension to make it easier to read::

    >>> df.unstack(level=0)
                               Bookings          ...
    Destination               Australia Denmark  ... Sweden United States
    Product            Grade                     ...
    Accommodation Only Bronze     10721       0  ...      0         20464
                       Gold           0       0  ...      0             0
                       Silver         0      45  ...    277             0
    Flight Only        Bronze    137883       0  ...      0         97440
                       Gold           0       0  ...      0             0
                       Silver         0     123  ...   2264             0
    Package Holiday    Bronze    134115       0  ...      0        443938
                       Gold           0       0  ...      0             0
                       Silver         0    1342  ...  22666             0

    [9 rows x 19 columns]

Using a base selection to filter the records::

    >>> sweden = dest == "29"
    >>> sweden_cube = sweden.cube([dest, product, grade])
    >>> sweden_df = sweden_cube.to_df()
    >>> sweden_df.head()
                                           Bookings
    Destination Product            Grade
    Australia   Accommodation Only Gold           0
                                   Silver         0
                                   Bronze         0
                Package Holiday    Gold           0
                                   Silver         0

Selecting only cells where ``Destination`` is *Sweden*,
and pivoting ``Product`` dimension::

    >>> sweden_df.loc["Sweden"].unstack(level=0)
                      Bookings
    Product Accommodation Only Flight Only Package Holiday
    Grade
    Bronze                   0           0               0
    Gold                     0           0               0
    Silver                 277        2264           22666

Using a base selection from a different table::

    >>> households = my_session.tables["Households"]
    >>> manchester = households["hoRegion"] == "13"
    >>> manc_cube = manchester.cube([dest, product, grade], table=bookings)
    >>> manc_df = manc_cube.to_df()
    >>> manc_df.loc["Germany"].unstack(level=1)
                       Bookings
    Grade                Bronze Gold Silver
    Product
    Accommodation Only      249    0      0
    Flight Only            4439    0      0
    Package Holiday        9882    0      0

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
    :param Clause selection: Base selection to apply to the cube.
        The table of this selection must be a 'related' table
        – either an ancestor or descendant.
    :param Table table: resolve table of the cube.
        This table's records are used in the analysis for the cube,
        e.g. the default count measure is counts records from this table.
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
            ...     table=bookings,
            ...     session=my_session,
            ... )
            >>> cube2 = Cube(
            ...     dimensions,
            ...     selection=(bookings * manchester),
            ...     session=my_session,
            ... )

        They both return a cube summarising *bookings* made by people
        from households in the Greater Manchester region.

    .. note::
        The raw cube data is fetched from the Apteco API
        when the :class:`Cube` object is initialised.
        It is held on the object in the :attr:`_data` attribute as a Numpy :class:`array`
        but this is not considered public, and so to work with the data
        you should convert it to your desired output format.
        The format currently supported is a Pandas :class:`DataFrame`,
        via the the :meth:`to_df` method.

    .. method:: to_df(unclassified=False, totals=False, no_trans=False, convert_index=True)

        Return the cube as a Pandas :class:`DataFrame`.

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
            'natural' Pandas index type.
            If *totals* or *no_trans* is *True*, this will be set to *False*.
            Default is `True`.

        The :class:`DataFrame` is configured such that:

            * the dimensions form the *index*.
              If multiple dimensions are given, this is a :class:`MultiIndex`,
              with each level corresponding to a dimension.
            * there is one *column* for each measure.

        .. tip::
            The structure of the DataFrame returned by the :meth:`to_df()` method
            is very similar to a *Tree* in the FastStats application.

        .. note::
            The Cube returns pre-calculated totals,
            which can be found under the *TOTAL* label on each dimension.
            You may need to filter these out if you are doing further analysis.

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

Date and DateTime variables cannot be used directly as cube dimensions,
but they can be banded up to a particular time period.
These bandings are access via attributes on the :class:`DateVariable`
or :class:`DateTimeVariable` object.

The following bandings are currently supported:

* ``DateVariable.day``
* ``DateVariable.month``
* ``DateVariable.quarter``
* ``DateVariable.year``

Conversion to a pandas DataFrame:

* The default index conversion is to a pandas :class:`PeriodIndex`
  with the corresponding frequency.
* If not converted, the index labels are the banded category descriptions.
* The index name is of the form `'Variable description (banding)'`.

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
will be added by default.

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

These statistics accept either a **selector** or **numeric** variable as the operand:


.. class:: CountMode

    The number of records which take the modal value of the variable.


.. class:: CountDistinct

    The number of distinct values of the variable.


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

