.. _cube_reference:

*********
  Cubes
*********

.. py:currentmodule:: apteco.cube


Introduction
============

The :class:`Cube` object corresponds to a FastStats Cube
and is a multi-dimensional numeric analysis of FastStats data.

The cube is specified by:

    * a resolve **table** – statistics in the cube are measures of
      records in this table
    * a set of **dimensions** – these are the fields over which the data
      is being summarised
    * a set of **measures** – these define the statistics displayed in the cube
      to summarise the data
    * a base **selection** *(optional)* – this filters records in the table
      to only include in the summary ones that match the given criteria

.. note::
    The cube functionality is still under active development,
    and so is currently subject to a couple of limitations:

    * The cube dimensions must be FastStats **Selector** variables
      (other variable types and more complex types like expressions
      are not currently supported).
    * Only the default *count* is supported as a measure,
      and this is set automatically.

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
    >>> manc_cube = bookings.cube([dest, product, grade], selection=manchester)
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

.. class:: Cube(dimensions, measures=None, selection=None, table=None, *, session=None)

    Create a cube.

    .. note::
        The :meth:`cube` methods on tables and selections are wrappers
        around this class.
        It is recommended to prefer those over instantiating this class directly,
        as they generally provide a simpler interface.

    :param list[Variable] dimensions: variables to use as dimensions in the cube.
        These must be from `table` or from a 'related' table
        – either an ancestor or descendant.
    :param measures: measures to display in the cube
        (default is :const:`None`, which will return the default `count` measure
        – this is the only option currently supported)
    :param Clause selection: base selection to apply to the cube.
        The table of this selection must be a 'related' table
        – either an ancestor or descendant.
    :param Table table: resolve table of the cube.
        This table's records used in the analysis for the cube,
        e.g. the `count` measure is counting records from this table.
    :param Session session: current Apteco API session.

    .. note::
        The only measure currently supported is the default count.
        The `measures` parameter is primarily included now
        for forward-compatibility,
        and must be set to :const:`None` (which is its default value).

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
        The only format currently supported is a Pandas :class:`DataFrame`.

    .. method:: to_df()

        Return the cube as a Pandas :class:`DataFrame`.

        The :class:`DataFrame` is configured such that:

            * the *index* is a :class:`MultiIndex`,
              with each level corresponding to a dimension
            * there is one *column* which is the single (default) `count` measure,
              named after resolve table of the cube
            * the index labels are the dimension category descriptions,
              rather than codes
            * all data values are integers, since they represent a count

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
