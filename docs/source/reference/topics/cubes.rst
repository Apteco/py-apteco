*********
  Cubes
*********

.. py:currentmodule:: apteco.cube


Introduction
============

The :class:`Cube` object corresponds to a FastStats Cube
and is a summary of FastStats data.

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
    and so is currently subject to several limitations:

    * The cube dimensions must be FastStats **Selector** variables
      (other variable types and more complex types like expressions
      are not currently supported).
    * Only the default *count* is supported as a measure,
      and this is set automatically.
    * The variables for the dimensions must be from the same table
      as the resolve table of the cube.

Basic use
=========

Importing :class:`Cube` and setting up other variables::

    >>> from apteco import Cube
    >>> bookings = my_session.tables["Bookings"]
    >>> dest = bookings["boDest"]
    >>> product = bookings["boProd"]
    >>> grade = bookings["deGrade"]

Creating a cube::

    >>> cube = Cube([dest, product, grade], table=bookings, session=my_session)

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

    >>>df.unstack(level=0)
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
    >>> cube_sweden = Cube([dest, product, grade], selection=sweden, session=my_session)
    >>> df_sweden = cube_sweden.to_df()
    >>> df_sweden.head()
                                            Bookings
    Destination  Product      Grade
    Unclassified Unclassified Unclassified         0
                              Gold                 0
                              Silver               0
                              Bronze               0
                              TOTAL                0

Selecting only cells where ``Destination`` is *Sweden*,
and pivoting ``Product`` dimension::

    >>> df_sweden.loc["Sweden"].unstack(level=0)
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
    >>> cube_manc = Cube(
            [dest, product, grade],
            selection=manchester,
            table=bookings,
            session=my_session,
        )
    >>> df_manc = cube_manc.to_df()
    >>> df_manc.loc["Germany"].unstack(level=1)
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

    :param list[Variable] dimensions: variables to use as dimensions in the cube
    :param measures: measures to display in the cube
        (default is *None*, which will return the default *count* measure
        – this is the only option currently supported)
    :param Clause selection: base selection to apply to the cube
    :param Table table: resolve table of the cube
    :param Session session: current Apteco API session

    .. note::

        The only measure currently supported is the default *count*.
        The :attr:`measures` parameter is primarily included now
        for forward-compatibility,
        and must be set to ``None`` (which is its default value).

    At least one of :attr:`selection` or :attr:`table` must be given:

        * If only :attr:`selection` is given,
          then :attr:`table` will be set to the resolve table of the selection.
        * If both are given and the resolve table of :attr:`selection`
          isn't :attr:`table`,
          then the records used in the cube
          are determined by mapping the selection to the required table by applying
          **ANY**/**THE** logic as necessary.
          This matches the behaviour when applying an underlying selection
          to a cube in the FastStats application.
          The mapping described here happens in the FastStats data engine
          and does not change the :attr:`selection` on the :class:`Cube`.

    .. tip::

        The following two cubes are equivalent::

            >>> cube1 = Cube(
                    dimensions,
                    selection=manchester,
                    table=bookings,
                    session=my_session,
                )
            >>> cube2 = Cube(
                    dimensions,
                    selection=(bookings * manchester),
                    session=my_session,
                )

        They both return a cube summarising *bookings* made by people
        from households in the Greater Manchester region.

    .. note::

        The raw cube data is fetched from the Apteco API
        when the :class:`Cube` object is initialised.
        It is held on the object in the :attr:`_data` attribute as a Numpy :class:`array`
        but this is not considered public, and so to work with the data
        you should convert it to your desired output format.
        The only format currently supported is a Pandas :class:`DataFrame`
        but other formats will be added in future.

    .. method:: to_df()

        Return the cube as a Pandas :class:`DataFrame`.

        Currently, the :class:`DataFrame` is configured such that:

            * the *index* is a :class:`MultiIndex`,
              with each level corresponding to a dimension
            * there is one *column* which is the single (default) count measure,
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

        For more details on working with a Pandas DataFrame
        with a MultiIndex,
        see the `user guide
        <https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html>`_
        in the official Pandas documentation.
