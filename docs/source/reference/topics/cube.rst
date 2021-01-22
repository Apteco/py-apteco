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
    Currently, the cube dimensions must be FastStats **Selector** variables.
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
    Destination  Product            Grade
    Unclassified Unclassified       Unclassified         0
                                    Gold                 0
                                    Silver               0
                                    Bronze               0
                                    TOTAL                0
                 Accommodation Only Unclassified     67012
                                    Gold                 0
                                    Silver               0
                                    Bronze               0
                                    TOTAL            67012

Pivoting the ``Destination`` dimension to make it easier to read::

    >>> df.unstack(level=0)
                                     Bookings          ...
    Destination                     Australia Denmark  ... Unclassified United States
    Product            Grade                           ...
    Accommodation Only Bronze           10721       0  ...            0         20464
                       Gold                 0       0  ...            0             0
                       Silver               0      45  ...            0             0
                       TOTAL            10721      45  ...        67012         20464
                       Unclassified         0       0  ...        67012             0
    Flight Only        Bronze          137883       0  ...            0         97440
                       Gold                 0       0  ...            0             0
                       Silver               0     123  ...            0             0
                       TOTAL           137883     123  ...            0         97440
                       Unclassified         0       0  ...            0             0
    Package Holiday    Bronze          134115       0  ...            0        443938
                       Gold                 0       0  ...            0             0
                       Silver               0    1342  ...            0             0
                       TOTAL           134115    1342  ...            0        443938
                       Unclassified         0       0  ...            0             0
    TOTAL              Bronze          282719       0  ...            0        561842
                       Gold                 0       0  ...            0             0
                       Silver               0    1510  ...            0             0
                       TOTAL           282719    1510  ...        67012        561842
                       Unclassified         0       0  ...        67012             0
    Unclassified       Bronze               0       0  ...            0             0
                       Gold                 0       0  ...            0             0
                       Silver               0       0  ...            0             0
                       TOTAL                0       0  ...            0             0
                       Unclassified         0       0  ...            0             0

    [25 rows x 21 columns]

Using a base selection to filter the records::

    >>> sweden = dest == "29"
    >>> sweden_cube = sweden.cube([dest, product, grade])
    >>> sweden_df = sweden_cube.to_df()
    >>> sweden_df.head()
                                            Bookings
    Destination  Product      Grade
    Unclassified Unclassified Unclassified         0
                              Gold                 0
                              Silver               0
                              Bronze               0
                              TOTAL                0

Selecting only cells where ``Destination`` is *Sweden*,
and pivoting ``Product`` dimension::

    >>> sweden_df.loc["Sweden"].unstack(level=0)
                               Bookings
    Product      Accommodation Only Flight Only Package Holiday  TOTAL Unclassified
    Grade
    Bronze                        0           0               0      0            0
    Gold                          0           0               0      0            0
    Silver                      277        2264           22666  25207            0
    TOTAL                       277        2264           22666  25207            0
    Unclassified                  0           0               0      0            0

Using a base selection from a different table::

    >>> households = my_session.tables["Households"]
    >>> manchester = households["hoRegion"] == "13"
    >>> manc_cube = manchester.cube([dest, product, grade], table=bookings)
    >>> manc_df = manc_cube.to_df()
    >>> manc_df.loc["Germany"].unstack(level=1)
                       Bookings
    Grade                Bronze Gold Silver  TOTAL Unclassified
    Product
    Accommodation Only      249    0      0    249            0
    Flight Only            4439    0      0   4439            0
    Package Holiday        9882    0      0   9882            0
    TOTAL                 14570    0      0  14570            0
    Unclassified              0    0      0      0            0

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
        If `measures` is None, the count measure of the cube's resolve table
        will be used by default.
    :param Clause selection: Base selection to apply to the cube.
        The table of this selection must be a 'related' table
        – either an ancestor or descendant.
    :param Table table: resolve table of the cube.
        This table's records are used in the analysis for the cube,
        e.g. the default count measure is counts records from this table.
    :param Session session: Current Apteco API session.

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

    .. method:: to_df()

        Return the cube as a Pandas :class:`DataFrame`.

        The :class:`DataFrame` is configured such that:

            * the dimensions form the *index*.
              If multiple dimensions are given, this is a :class:`MultiIndex`,
              with each level corresponding to a dimension.
              The index labels are the dimension category descriptions.
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

.. class:: Mode

    The mode (most common) value of the variable.


.. class:: CountMode

    The number of records which take the modal value of the variable.


.. class:: CountDistinct

    The number of distinct values of the variable.


These statistics accept a **numeric** variable as the operand:

.. class:: Populated

    The number of records for which the variable has a (non-missing) value.


.. class:: Sum

    The sum of values of the variable.


.. class:: Min

    The minimum value of the variable.


.. class:: Max

    The maximum value of the variable.


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

