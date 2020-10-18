***********************
  Creating Data Grids
***********************

Exporting data into a data grid makes it available in a format
that lets us easily carry out further analysis on it.
In this part of the tutorial we'll learn how to create data grids,
and how to control what data is exported into them.

Creating a data grid
====================

We can use the :meth:`datagrid` method on a table
to create a data grid showing records from that table.
We pass it a list of the FastStats variables we want to use as data grid columns::

    >>> pol_num = policies["Policy Number"]
    >>> pol_date = policies["Policy Date"]
    >>> premium = policies["Premium"]
    >>> cover = policies["Cover"]
    >>> days_to_travel = policies["Days Until Travel"]
    >>> dg = policies.datagrid([pol_num, pol_date, premium, cover, days_to_travel])

To work with the data we can convert it to a Pandas :class:`DataFrame`
using the :meth:`to_df()` method::

    >>> df = dg.to_df()
    >>> df
        Policy Number Policy Date  Premium        Cover  Days Until Travel
    0        10001265  2019-05-21    87.02   Individual                 25
    1        10036397  2017-04-09   123.30   Individual                 91
    2        10078565  2018-09-05   143.20   Multi Trip                 30
    3        10078566  2018-10-07    29.23       Family                 60
    4        10078567  2018-10-03    14.65  Single Trip                 10
    ..            ...         ...      ...          ...                ...
    995      11192414  2022-01-06    17.83  Single Trip                 26
    996      11205561  2016-07-09    10.43   Individual                 35
    997      11242733  2021-02-23    33.56   Individual                 10
    998      11252163  2021-03-23    13.57   Individual                 41
    999      11262841  2020-07-28    11.19   Individual                 86

    [1000 rows x 5 columns]

Where possible, the :meth:`to_df()` method will convert the raw data
to the corresponding native data types::

    >>> df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1000 entries, 0 to 999
    Data columns (total 5 columns):
     #   Column             Non-Null Count  Dtype
    ---  ------             --------------  -----
     0   Policy Number      1000 non-null   object
     1   Policy Date        1000 non-null   object
     2   Premium            1000 non-null   float64
     3   Cover              1000 non-null   object
     4   Days Until Travel  1000 non-null   int64
    dtypes: float64(1), int64(1), object(3)
    memory usage: 39.2+ KB

Pandas doesn't currently have a column type for strings or dates
(though it does have a date\ *time* column type),
so these are stored as ordinary Python objects.
However if we select an individual string or date from the DataFrame
we can see that it's a native :class:`str` or :class:`datetime.date`::

    >>> df.loc[2, "Cover"]
    'Multi Trip'
    >>> df.loc[3, "Policy Date"]
    datetime.date(2018, 10, 7)

You can use any variable type as a data grid column,
except for Array and Flag Array variables.
As in FastStats, you can also use variables from parent or ancestor tables,
but not child or descendant tables::

    >>> occupation = people["Occupation"]
    >>> town = households["Town"]
    >>> mixed_tables_dg = policies.datagrid([pol_num, premium, occupation, cover, town])
    >>> mixed_tables_dg.to_df()
        Policy Number  Premium        Cover       Occupation                 Town
    0        10001265    87.02   Individual  Sales Executive             Aberdeen
    1        10036397   123.30   Individual     Professional           Birmingham
    2        10078565   143.20   Multi Trip  Sales Executive     Sutton Coldfield
    3        10078566    29.23       Family  Sales Executive     Sutton Coldfield
    4        10078567    14.65  Single Trip    Public Sector     Sutton Coldfield
    ..            ...      ...          ...              ...                  ...
    995      11192414    17.83  Single Trip    Retail Worker            Maidstone
    996      11205561    10.43   Individual    Public Sector           Buckingham
    997      11242733    33.56   Individual         Director               London
    998      11252163    13.57   Individual    Public Sector  Newcastle-upon-Tyne
    999      11262841    11.19   Individual    Public Sector  Newcastle-upon-Tyne

    [1000 rows x 5 columns]

.. note::
    This is the table structure for the tables
    from the demo *Holidays* system being used here::

        Households
         └─ People
             └─ Policies

    Our data grid is displaying `Policies` records, but the columns include
    the `Occupation` variable from the parent `People` table,
    as well as the `Town` variable from the 'grandparent' `Households` table.

Controlling the number of rows
==============================

By default, the data grid will return 1000 rows,
but we can adjust this using the `max_rows` parameter::

    >>> columns = [pol_num, premium, occupation, cover, town]
    >>> only_10_policies_dg = policies.datagrid(columns, max_rows=10)
    >>> only_10_policies_dg.to_df()
      Policy Number  Premium       Occupation        Cover              Town
    0      10001265    87.02  Sales Executive   Individual          Aberdeen
    1      10036397   123.30     Professional   Individual        Birmingham
    2      10078565   143.20  Sales Executive   Multi Trip  Sutton Coldfield
    3      10078566    29.23  Sales Executive       Family  Sutton Coldfield
    4      10078567    14.65    Public Sector  Single Trip  Sutton Coldfield
    5      10090306    30.50     Professional       Family          Redditch
    6      10094721    83.78    Public Sector       Family              Bath
    7      10109667    25.48          Manager   Individual            Yeovil
    8      10109674    33.87    Public Sector   Multi Trip            Yeovil
    9      10123545    50.56  Sales Executive   Individual            Nelson

.. note::
    As its name suggests, the number of rows in the data grid
    isn't necessarily equal to `max_rows` – it just provides an upper limit.
    The number of rows will be less than this
    if there are fewer records available.

Applying a selection
====================

You can filter the records shown in the data grid by applying a selection to it
using the `selection` parameter::

    >>> multi_trip = policies["Cover"] == "4"
    >>> multi_trip_dg = policies.datagrid(columns, selection=multi_trip)
    >>> multi_trip_dg.to_df()
        Policy Number  Premium       Occupation       Cover              Town
    0        10078565   143.20  Sales Executive  Multi Trip  Sutton Coldfield
    1        10109674    33.87    Public Sector  Multi Trip            Yeovil
    2        10278405    56.27  Sales Executive  Multi Trip             Newry
    3        10326709    21.99  Sales Executive  Multi Trip         Cambridge
    4        10425299    38.50          Student  Multi Trip     South Croydon
    ..            ...      ...              ...         ...               ...
    995      10976366    87.88  Sales Executive  Multi Trip             Esher
    996      11131381    14.12       Unemployed  Multi Trip            Pudsey
    997      11258013   148.09    Public Sector  Multi Trip         Gateshead
    998      11519086    45.61  Sales Executive  Multi Trip      Bognor Regis
    999      11783140    12.66     Professional  Multi Trip        Malmesbury

    [1000 rows x 5 columns]

You can also build the data grid directly
from the selection using the :meth:`datagrid` method::

    >>> multi_trip_dg = multi_trip.datagrid(columns)
    >>> multi_trip_dg.to_df()
        Policy Number  Premium       Occupation       Cover              Town
    0        10078565   143.20  Sales Executive  Multi Trip  Sutton Coldfield
    1        10109674    33.87    Public Sector  Multi Trip            Yeovil
    2        10278405    56.27  Sales Executive  Multi Trip             Newry
    3        10326709    21.99  Sales Executive  Multi Trip         Cambridge
    4        10425299    38.50          Student  Multi Trip     South Croydon
    ..            ...      ...              ...         ...               ...
    995      10976366    87.88  Sales Executive  Multi Trip             Esher
    996      11131381    14.12       Unemployed  Multi Trip            Pudsey
    997      11258013   148.09    Public Sector  Multi Trip         Gateshead
    998      11519086    45.61  Sales Executive  Multi Trip      Bognor Regis
    999      11783140    12.66     Professional  Multi Trip        Malmesbury

    [1000 rows x 5 columns]

*(this data grid is identical to the previous one)*

When creating a data grid from a selection,
the table for the data grid is automatically set as the selection's table.

Applying a selection from a different table
===========================================

Just as in FastStats, you can apply a selection based on a table
different from the one used in your data grid::

    >>> student = people["Occupation"] == "4"
    >>> student_policies_dg = policies.datagrid(columns, selection=student)
    >>> student_policies_dg.to_df()
        Policy Number  Premium Occupation        Cover            Town
    0        10152036    33.82    Student  Single Trip     Bournemouth
    1        10165468    23.22    Student   Individual        Ferndown
    2        10173730   117.09    Student       Family          Bolton
    3        10415201    10.29    Student   Individual         Sudbury
    4        10418882    30.11    Student   Individual  Clacton-on-Sea
    ..            ...      ...        ...          ...             ...
    995      10204828    34.75    Student       Family      Eastbourne
    996      10423854    12.87    Student       Family         Croydon
    997      10467615    16.68    Student  Single Trip  Leamington Spa
    998      10597061    34.80    Student  Single Trip     Stourbridge
    999      10629056    17.79    Student   Individual          London

    [1000 rows x 5 columns]

Here, ``student`` is a selection on the `People` table,
but we are applying it to a `Policies` data grid.

Again, you can build the data grid from the selection itself,
but this time you will need to use the `table` parameter
to set the data grid to the desired table::

    >>> student_policies_dg = student.datagrid(columns, table=policies)
    >>> student_policies_dg.to_df()
        Policy Number  Premium Occupation        Cover            Town
    0        10152036    33.82    Student  Single Trip     Bournemouth
    1        10165468    23.22    Student   Individual        Ferndown
    2        10173730   117.09    Student       Family          Bolton
    3        10415201    10.29    Student   Individual         Sudbury
    4        10418882    30.11    Student   Individual  Clacton-on-Sea
    ..            ...      ...        ...          ...             ...
    995      10204828    34.75    Student       Family      Eastbourne
    996      10423854    12.87    Student       Family         Croydon
    997      10467615    16.68    Student  Single Trip  Leamington Spa
    998      10597061    34.80    Student  Single Trip     Stourbridge
    999      10629056    17.79    Student   Individual          London

    [1000 rows x 5 columns]

*(this data grid is identical to the previous one)*

As well as exporting data to a data grid to do further analysis on it externally,
FastStats has built-in support for many kinds of analysis.
In the next part, we'll learn how to create Cubes
for carrying out multi-dimensional tabular analysis on our data.
