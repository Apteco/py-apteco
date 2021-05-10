.. _datagrid_reference:

*************
  Data Grid
*************

.. py:currentmodule:: apteco.datagrid

Introduction
============

The :class:`DataGrid` object corresponds to a FastStats Data Grid
and is an exported set of data from the FastStats system.

The data to export is specified by:

    * a resolve **table** – each row in the data grid corresponds to
      a single record in this table
    * a set of **columns** – these are the fields of data returned for each record
    * a base **selection** *(optional)* – this filters records in the table
      to only return ones that match the given criteria

There are also other parameters that determine things such as
how many rows of data to return.

.. note::
    The data grid functionality is still under active development,
    and so is currently subject to a couple of limitations:

    * The data grid columns must be FastStats variables
      (expressions and other more complex column types are not currently supported)
    * **Array** and **FlagArray** variables are not currently supported as columns

Basic use
=========

Setting up variables::

    >>> bookings = my_session.tables["Bookings"]
    >>> urn = bookings["Booking URN"]
    >>> dest = bookings["Destination"]
    >>> trav = bookings["Travel Date"]
    >>> cost = bookings["Cost"]

Creating a data grid::

    >>> datagrid = bookings.datagrid([urn, dest, trav, cost])

Converting to a Pandas :class:`DataFrame`::

    >>> df = datagrid.to_df()
    >>> df.head()
      Booking URN   Destination Travel Date     Cost
    0    10001265        France  2019-05-15  1392.35
    1    10001266        France  2019-06-05   780.34
    2    10011532       Germany  2021-08-29   181.68
    3    10011533       Germany  2021-08-21   300.67
    4    10015830  Unclassified  2016-05-02   228.70

Specifying the number of rows to return::

    >>> datagrid = bookings.datagrid([urn, dest, trav, cost], max_rows=100)
    >>> df = datagrid.to_df()
    >>> len(df)
    100

Using a base selection to filter the records::

    >>> sweden = dest == "29"
    >>> sweden_datagrid = sweden.datagrid([urn, dest, trav, cost])
    >>> sweden_df = sweden_datagrid.to_df()
    >>> sweden_df.head()
      Booking URN Destination Travel Date     Cost
    0    10172319      Sweden  2020-05-15  1201.81
    1    10384970      Sweden  2018-04-05   344.30
    2    10421011      Sweden  2019-07-11   322.89
    3    10425298      Sweden  2020-10-10   880.02
    4    10479109      Sweden  2020-09-21   172.91

Using a base selection from a different table::

    >>> households = my_session.tables["Households"]
    >>> town = households["Town"]
    >>> postcode = households["Postcode"]
    >>> manchester = households["Region"] == "13"
    >>> manc_datagrid = manchester.datagrid([urn, dest, trav, cost, town, postcode], table=bookings)
    >>> manc_df = manc_datagrid.to_df()
    >>> manc_df.head()
      Booking URN    Destination Travel Date     Cost    Town Postcode
    0    10172319         Sweden  2020-05-15  1201.81  Bolton  BL1 5XB
    1    10172320  United States  2020-04-14  1616.80  Bolton  BL1 5XB
    2    10173729         France  2020-08-19   581.71  Bolton  BL1 8JJ
    3    10173730         France  2020-08-09  2224.70  Bolton  BL1 8JJ
    4    10177047         France  2021-05-07   686.53  Bolton  BL3 5LX

.. Data Grid-related tasks
.. =======================

API reference
=============

.. class:: DataGrid(columns, selection=None, table=None, *, session=None)

    Create a data grid.

    .. tip::
        The :meth:`datagrid` methods on tables and selections are wrappers
        around this class.
        It is recommended to prefer those over instantiating this class directly,
        as they generally provide a simpler interface.

    :param list[Variable] columns: variables to use as columns in the data grid.
        These must be from `table` or from one of its ancestor tables.
    :param Clause selection: base selection to apply to the data grid.
        The table of this selection must be `table` or a 'related' table
        – either an ancestor or descendant.
    :param Table table: resolve table of the data grid.
        Each row of the data grid will correspond to a record
        from this table.
    :param int max_rows: maximum number of records to return *(default is 1000)*.
    :param Session session: current Apteco API session.

    At least one of `selection` or `table` must be given:

        * If only `selection` is given,
          then `table` will be set to the resolve table of the selection.
        * If both are given and the resolve table of `selection`
          isn't `table`,
          then the records returned in the data grid
          are determined by mapping the selection to the required table by applying
          **ANY**/**THE** logic as necessary.
          This matches the behaviour when applying an underlying selection
          to a data grid in the FastStats application.
          The mapping described here happens in the FastStats data engine
          and does not change the `selection` on the :class:`DataGrid`.

    .. tip::
        The following two data grids are equivalent::

            >>> datagrid1 = DataGrid(
            ...     columns,
            ...     selection=manchester,
            ...     table=bookings,
            ...     session=my_session,
            ... )
            >>> datagrid2 = DataGrid(
            ...     columns,
            ...     selection=(bookings * manchester),
            ...     session=my_session,
            ... )

        They both return a data grid of *bookings* made by people
        from households in the Greater Manchester region.

    .. note::
        The raw data is fetched from the Apteco API
        when the :class:`DataGrid` object is initialised.
        It is held on the object in the :attr:`_data` attribute as a list of tuples
        but this is not considered public, and so to work with the data
        you should convert it to your desired output format.
        The only format currently supported is a Pandas :class:`DataFrame`.

    .. method:: to_df()

        Return the data as a Pandas :class:`DataFrame`.

        The :class:`DataFrame` is configured such that:

            * the *index* is a :class:`RangeIndex`
            * the *columns* (headings) are the variable descriptions
            * data is returned as its corresponding Pandas column type
              or native Python type
            * Selector variable columns contain strings of the category descriptions

        ::

            >>> pol_num = policies["Policy Number"]
            >>> premium = policies["Premium"]
            >>> cover = policies["Cover"]
            >>> dob = people["DOB"]
            >>> postcode = households["Postcode"]
            >>> policies_datagrid = policies.datagrid([pol_num, premium, cover, dob, postcode])
            >>> policies_datagrid.to_df()
                Policy Number  Premium        Cover         DOB  Postcode
            0        10001265    87.02   Individual  1975-02-09  AB10 1XL
            1        10036397   123.30   Individual  1972-11-25    B6 4TN
            2        10078565   143.20   Multi Trip  1971-10-05   B74 2QX
            3        10078566    29.23       Family  1971-10-05   B74 2QX
            4        10078567    14.65  Single Trip  1999-11-14   B74 2QX
            ..            ...      ...          ...         ...       ...
            995      11192414    17.83  Single Trip         NaT  ME15 0QB
            996      11205561    10.43   Individual  1976-01-30  MK18 7ZT
            997      11242733    33.56   Individual  1977-01-22   N16 7NJ
            998      11252163    13.57   Individual  1997-09-12   NE2 2DJ
            999      11262841    11.19   Individual  1978-08-03  NE20 9QJ

            [1000 rows x 5 columns]

        .. seealso::
            For more details on working with a Pandas DataFrame
            see the `official Pandas documentation
            <https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html>`_.
