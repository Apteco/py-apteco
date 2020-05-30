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

.. note::

    The data grid functionality is still under active development,
    and so is currently subject to several limitations:

    * The data grid columns must be FastStats variables
      (expressions and other more complex column types are not currently supported)
    * **Array** and **FlagArray** variables are not currently supported as columns
    * The variables for the columns must be from the same table
      as the resolve table of the data grid.

Basic use
=========

Importing :class:`DataGrid` and setting up other variables::

    >>> from apteco.datagrid import DataGrid
    >>> bookings = my_session.tables["Bookings"]
    >>> urn = bookings["boURN"]
    >>> dest = bookings["boDest"]
    >>> trav = bookings["boTrav"]
    >>> cost = bookings["boCost"]

Creating a data grid::

    >>> dg = DataGrid([urn, dest, trav, cost], table=bookings, session=my_session)

Converting to a Pandas :class:`DataFrame`::

    >>> df = dg.to_df()
    >>> df.head()
      Booking URN   Destination Travel Date          Cost
    0    10001265        France  15-05-2019       1392.35
    1    10001266        France  05-06-2019        780.34
    2    10011532       Germany  29-08-2021        181.68
    3    10011533       Germany  21-08-2021        300.67
    4    10015830  Unclassified  02-05-2016        228.70

Using a base selection to filter the records::

    >>> sweden = dest == "29"
    >>> dg = DataGrid([urn, dest, trav, cost], selection=sweden, session=my_session)
    >>> df = dg.to_df()
    >>> df.head()
      Booking URN Destination Travel Date          Cost
    0    10172319      Sweden  15-05-2020       1201.81
    1    10384970      Sweden  05-04-2018        344.30
    2    10421011      Sweden  11-07-2019        322.89
    3    10425298      Sweden  10-10-2020        880.02
    4    10479109      Sweden  21-09-2020        172.91

Using a base selection from a different table::

    >>> households = my_session.tables["Households"]
    >>> manchester = households["hoRegion"] == "13"
    >>> dg = DataGrid(
            [urn, dest, trav, cost],
            selection=manchester,
            table=bookings,
            session=my_session,
        )
    >>> df = dg.to_df()
    >>> df.head()
      Booking URN    Destination Travel Date          Cost
    0    10172319         Sweden  15-05-2020       1201.81
    1    10172320  United States  14-04-2020       1616.80
    2    10173729         France  19-08-2020        581.71
    3    10173730         France  09-08-2020       2224.70
    4    10177047         France  07-05-2021        686.53

.. Data Grid-related tasks
.. =======================

API reference
=============

.. class:: DataGrid(columns, selection=None, table=None, *, session=None)

    Create a data grid.

    :param list[Variable] columns: variables to use as columns in the data grid
    :param Clause selection: base selection to apply to the data grid
    :param Table table: resolve table of the data grid
    :param Session session: current Apteco API session

    At least one of :attr:`selection` or :attr:`table` must be given:

        * If only :attr:`selection` is given,
          then :attr:`table` will be set to the resolve table of the selection.
        * If both are given and the resolve table of :attr:`selection`
          isn't :attr:`table`,
          then the records returned in the data grid
          are determined by mapping the selection to the required table by applying
          **ANY**/**THE** logic as necessary.
          This matches the behaviour when applying an underlying selection
          to a data grid in the FastStats application.
          The mapping described here happens in the FastStats data engine
          and does not change the :attr:`selection` on the :class:`DataGrid`.

.. tip::

    The following two data grids are equivalent::

        >>> dg1 = DataGrid(
                columns,
                selection=manchester,
                table=bookings,
                session=my_session,
            )
        >>> dg2 = DataGrid(
                columns,
                selection=(bookings * manchester),
                session=my_session,
            )

    They both return a data grid of *bookings* made by people
    from households in the Greater Manchester region.

.. note::

    The raw data is fetched from the Apteco API
    when the :class:`DataGrid` object is initialised.
    It is held on the object in the :attr:`_data` attribute as a list of tuples
    but this is not considered public, and so to work with the data
    you should convert it to your desired output format.
    The only format currently supported is a Pandas :class:`DataFrame`
    but other formats will be added in future.

.. method:: to_df()

    Return the data as a Pandas :class:`DataFrame`.

    Currently, the :class:`DataFrame` is configured such that:

        * the *index* is a :class:`RangeIndex`
        * the *columns* are the variable descriptions
        * Selector, Date and DateTime variable columns display descriptions,
          rather than codes
        * all data is returned as raw strings
