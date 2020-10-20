.. _datagrid_reference:

**************
  Data Grids
**************

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

    >>> dg = bookings.datagrid([urn, dest, trav, cost])

Converting to a Pandas :class:`DataFrame`::

    >>> df = dg.to_df()
    >>> df.head()
      Booking URN   Destination Travel Date     Cost
    0    10001265        France  2019-05-15  1392.35
    1    10001266        France  2019-06-05   780.34
    2    10011532       Germany  2021-08-29   181.68
    3    10011533       Germany  2021-08-21   300.67
    4    10015830  Unclassified  2016-05-02   228.70

Specifying the number of rows to return::

    >>> dg = bookings.datagrid([urn, dest, trav, cost], max_rows=100)
    >>> df = dg.to_df()
    >>> len(df)
    100

Using a base selection to filter the records::

    >>> sweden = dest == "29"
    >>> sweden_dg = sweden.datagrid([urn, dest, trav, cost])
    >>> sweden_df = sweden_dg.to_df()
    >>> sweden_df.head()
      Booking URN Destination Travel Date     Cost
    0    10172319      Sweden  2020-05-15  1201.81
    1    10384970      Sweden  2018-04-05   344.30
    2    10421011      Sweden  2019-07-11   322.89
    3    10425298      Sweden  2020-10-10   880.02
    4    10479109      Sweden  2020-09-21   172.91

Using a base selection from a different table::

    >>> households = my_session.tables["Households"]
    >>> manchester = households["Region"] == "13"
    >>> manc_dg = bookings.datagrid([urn, dest, trav, cost], selection=manchester)
    >>> manc_df = manc_dg.to_df()
    >>> manc_df.head()
      Booking URN    Destination Travel Date     Cost
    0    10172319         Sweden  2020-05-15  1201.81
    1    10172320  United States  2020-04-14  1616.80
    2    10173729         France  2020-08-19   581.71
    3    10173730         France  2020-08-09  2224.70
    4    10177047         France  2021-05-07   686.53

.. Data Grid-related tasks
.. =======================

API reference
=============

.. class:: DataGrid(columns, selection=None, table=None, *, session=None)

    Create a data grid.

    .. note::
        The :meth:`datagrid` methods on tables and selections are wrappers
        around this class.
        It is recommended to prefer those over instantiating this class directly,
        as they generally provide a simpler interface.

    :param list[Variable] columns: variables to use as columns in the data grid.
        These must be from `table` or from one of its ancestor tables.
    :param Clause selection: base selection to apply to the data grid.
        The table of this selection must be a 'related' table
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

        >>> dg1 = DataGrid(
        ...     columns,
        ...     selection=manchester,
        ...     table=bookings,
        ...     session=my_session,
        ... )
        >>> dg2 = DataGrid(
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
        * the *columns* are the variable descriptions
        * Selector, Date and DateTime variable columns display descriptions,
          rather than codes
        * data is returned as its corresponding Pandas column type
          or native Python type

        .. seealso::
            For more details on working with a Pandas DataFrame
            see the `official Pandas documentation
            <https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html>`_.
