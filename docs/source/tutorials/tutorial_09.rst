******************
  Creating Cubes
******************

A cube is a numeric analysis showing data
broken down by one or more dimensions.
In this part of the tutorial we'll learn how to create cubes,
and how to control what data is included in them.

Creating a cube
===============

We can use the :meth:`cube` method on a table
to create a cube analysing records from that table.
We pass it a list of the FastStats variables we want to use as cube dimensions::

    >>> occupation = people["Occupation"]
    >>> income = people["Income"]
    >>> gender = people["Gender"]
    >>> cube = people.cube([occupation, income, gender])

If we don't specify any measures, the `count` measure is used by default.

To work with the data we can convert it to a Pandas :class:`DataFrame`
using the :meth:`to_df()` method::

    >>> df = cube.to_df()
    >>> df
                                    People
    Occupation    Income   Gender
    Manual Worker <£10k    Female    15624
                           Male       5321
                           Unknown       5
                  £10-20k  Female    43051
                           Male       5992
                                    ...
    Retired       £90-100k Male          2
                           Unknown       0
                  £100k+   Female        0
                           Male          1
                           Unknown       0

    [330 rows x 1 columns]

The DataFrame uses a `MultiIndex
<https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.MultiIndex.html>`_,
with each dimension as a different level in the index::

    >>> df.index
    MultiIndex([('Manual Worker',    '<£10k',  'Female'),
            ('Manual Worker',    '<£10k',    'Male'),
            ('Manual Worker',    '<£10k', 'Unknown'),
            ('Manual Worker',  '£10-20k',  'Female'),
            ('Manual Worker',  '£10-20k',    'Male'),
            ('Manual Worker',  '£10-20k', 'Unknown'),
            ('Manual Worker',  '£20-30k',  'Female'),
            ('Manual Worker',  '£20-30k',    'Male'),
            ('Manual Worker',  '£20-30k', 'Unknown'),
            ('Manual Worker',  '£30-40k',  'Female'),
            ...
            (      'Retired',  '£70-80k', 'Unknown'),
            (      'Retired',  '£80-90k',  'Female'),
            (      'Retired',  '£80-90k',    'Male'),
            (      'Retired',  '£80-90k', 'Unknown'),
            (      'Retired', '£90-100k',  'Female'),
            (      'Retired', '£90-100k',    'Male'),
            (      'Retired', '£90-100k', 'Unknown'),
            (      'Retired',   '£100k+',  'Female'),
            (      'Retired',   '£100k+',    'Male'),
            (      'Retired',   '£100k+', 'Unknown')],
           names=['Occupation', 'Income', 'Gender'], length=330)

The DataFrame has one column which is the default count measure,
named after the entity it is counting.
Since the data values represent a count, they are all integers::

    >>> df.info()
    <class 'pandas.core.frame.DataFrame'>
    MultiIndex: 330 entries, ('Manual Worker', '<£10k', 'Female') to ('Retired', '£100k+', 'Unknown')
    Data columns (total 1 columns):
     #   Column  Non-Null Count  Dtype
    ---  ------  --------------  -----
     0   People  330 non-null    int64
    dtypes: int64(1)
    memory usage: 4.6+ KB

More generally, the DataFrame will have one column
for each measure included on the cube.

.. tip::
    This initial structure of the DataFrame returned by the :meth:`to_df()` method
    is very similar to a *Tree* in the FastStats application.

Pivoting the ``Gender`` dimension returns a :class:`DataFrame`
with ``Gender`` as a new level of column labels.
You may find this arrangement easier to read
and more similar to how a cube would be presented in FastStats::

    >>> df.unstack(level=2)
                        People
    Gender              Female  Male Unknown
    Occupation Income
    Director   <£10k      1279   832       4
               £10-20k    4116  2139       9
               £100k+        2     1       1
               £20-30k    1267  1050       5
               £30-40k    1591  1940      46
                        ...   ...     ...
    Unemployed £50-60k     277    69      89
               £60-70k      58     8      17
               £70-80k      27     5       5
               £80-90k       0     0       0
               £90-100k      1     0       0

    [110 rows x 3 columns]

As well as Selector variables,
you can also use banded Date or Datetime variables as cube dimensions.
These bandings are accessible as attributes on the variable::

    >>> dest = bookings["Destination"]
    >>> booking_date = bookings["Booking Date"]
    >>> booking_year_by_dest = bookings.cube([booking_date.year, dest])
    >>> year_dest_df = booking_year_by_dest.to_df()
    >>> year_dest_df.unstack(level=0)
                        Bookings
    Booking Date (Year)     2016   2017    2018   2019    2020    2021
    Destination
    Australia              28747  32766   68271  46576   54519   51840
    Denmark                  158    169     355    244     299     285
    France                 51950  60253  125838  85903  102543   97987
    Germany                47031  53691  109053  75120   89974   86391
    Greece                 11220  12999   27145  18558   21797   20373
    Italy                   3557   4272    8704   6065    7200    7083
    Jamaica                   19     14      42     32      38      34
    Kuwait                  2373   2765    5546   3907    4550    4407
    Latvia                    69     78     168    107     102     121
    Mali                     104    122     215    136     209     188
    Mongolia                  24     17      38     15      32      28
    Namibia                  250    254     553    385     476     431
    New Zealand               93    109     227    113     178     159
    Portugal                2222   2514    5124   3560    4184    4028
    Senegal                  111    109     238    183     159     181
    Sierra Leone             466    613    1081    787     938     902
    South Africa              88    119     208    164     199     178
    Sweden                  2460   2915    6120   4112    4929    4671
    United States          58691  64546  134846  92003  108080  103676

The supported bandings are: ``year``, ``quarter``, ``month``, ``day``

Banded Date variables use a `PeriodIndex <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#periodindex-and-period-range>`_
in the outputted Dataframe::

    >>> travel_date = bookings["Travel Date"]
    >>> travel_month_df = bookings.cube([travel_date.month]).to_df()
    >>> travel_month_df
                         Bookings
    Travel Date (Month)
    2016-01                   410
    2016-02                  4059
    2016-03                 12233
    2016-04                 20175
    2016-05                 25601
                           ...
    2022-08                     0
    2022-09                     0
    2022-10                     0
    2022-11                     0
    2022-12                     0

    [84 rows x 1 columns]
    >>> travel_month_df.index
    PeriodIndex(['2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06',
                 '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12',
                 '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06',
                 '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12',
                 '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06',
                 '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
                 '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
                 '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
                 '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06',
                 '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
                 '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06',
                 '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12',
                 '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06',
                 '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12'],
                dtype='period[M]', name='Travel Date (Month)', freq='M')

As in FastStats, you can also use variables from 'related' tables,
that is, ancestor or descendant tables (including the direct parent and children)::

    >>> region = households["Region"]
    >>> continent = bookings["Continent"]
    >>> mixed_tables_cube = people.cube([region, occupation, continent])
    >>> mixed_tables_cube.to_df()
                                               People
    Region          Occupation    Continent
    North           Manual Worker Australasia     101
                                  Europe         4158
                                  Americas         96
                                  Asia              2
                                  Africa            2
                                               ...
    Channel Islands Retired       Australasia       7
                                  Europe           18
                                  Americas         10
                                  Asia              2
                                  Africa            2

    [700 rows x 1 columns]

.. note::
    This is the table structure for the tables
    from the demo *Holidays* system being used here::

        Households
         └─ People
             └─ Bookings

    Our cube is showing a count of `People` records, but the dimensions include
    the `Region` variable from the parent `Households` table,
    as well as the `Continent` variable from the child `Bookings` table.

Controlling DataFrame output
============================

By default, the DataFrame returned by :meth:`to_df()` doesn't include
unclassified values or totals.
But these can be included by setting the ``unclassified`` and ``totals`` arguments
(respectively) for :meth:`to_df()` to :const:`True`::

    >>> gender_cube = people.cube([gender])
    >>> gender_cube.to_df()
             People
    Gender
    Female   764796
    Male     378567
    Unknown   13190
    >>> gender_cube.to_df(unclassified=True, totals=True)
                   People
    Gender
    Unclassified        0
    Female         764796
    Male           378567
    Unknown         13190
    TOTAL         1156553

If any of these extra values are included for a cube with a Banded Date dimension,
the corresponding DataFrame index cannot be converted to a :class:`PeriodIndex`
so will be left as a plain :class:`Index`::

    >>> booking_year_cube = bookings.cube([booking_date.year])
    >>> booking_year_cube.to_df().index
    PeriodIndex(['2016', '2017', '2018', '2019', '2020', '2021'], dtype='period[A-DEC]', name='Booking Date (Year)', freq='A-DEC')
    >>> booking_year_cube.to_df(unclassified=True).index
    Index(['Unclassified', '2016', '2017', '2018', '2019', '2020', '2021'], dtype='object', name='Booking Date (Year)')

To stop the index being automatically converted to a :class:`PeriodIndex`
even when these extra values *aren't* included,
set the ``convert_index`` argument to :const:`False`::

    >>> booking_year_cube.to_df(convert_index=False).index
    Index(['2016', '2017', '2018', '2019', '2020', '2021'], dtype='object', name='Booking Date (Year)')

Applying a selection
====================

You can filter the records used in the analysis for the cube
by applying a selection to it using the `selection` parameter::

    >>> student = people["Occupation"] == "4"
    >>> student_cube = people.cube([occupation, region, continent], selection=student)
    >>> student_cube.to_df()
                                               People
    Occupation    Region          Continent
    Manual Worker North           Australasia       0
                                  Europe            0
                                  Americas          0
                                  Asia              0
                                  Africa            0
                                               ...
    Retired       Channel Islands Australasia       0
                                  Europe            0
                                  Americas          0
                                  Asia              0
                                  Africa            0

    [700 rows x 1 columns]

You can also build the cube directly
from the selection using the :meth:`cube` method::

    >>> student_cube = student.cube([occupation, region, continent])
    >>> student_cube.to_df()
                                               People
    Occupation    Region          Continent
    Manual Worker North           Australasia       0
                                  Europe            0
                                  Americas          0
                                  Asia              0
                                  Africa            0
                                               ...
    Retired       Channel Islands Australasia       0
                                  Europe            0
                                  Americas          0
                                  Asia              0
                                  Africa            0

    [700 rows x 1 columns]

*(this cube is identical to the previous one)*

When creating a data grid from a selection,
the table for the data grid is automatically set as the selection's table.

Applying a selection from a different table
===========================================

Just as in FastStats, you can apply a selection based on a table
different from the one used in your cube::

    >>> scotland = region == "10"
    >>> scotland_cube = people.cube([occupation, region, continent], selection=scotland)
    >>> scotland_cube.to_df()
                                               People
    Occupation    Region          Continent
    Manual Worker North           Australasia       0
                                  Europe            0
                                  Americas          0
                                  Asia              0
                                  Africa            0
                                               ...
    Retired       Channel Islands Australasia       0
                                  Europe            0
                                  Americas          0
                                  Asia              0
                                  Africa            0

    [700 rows x 1 columns]

Here, ``scotland`` is a selection on the `Households` table,
but we are applying it to a `People` cube.

.. note::
    The selection's table must be a 'related' table
    – either an ancestor or descendant.

Again, you can build the cube from the selection itself,
but this time you will need to use the `table` parameter
to set the cube to the desired table::

    >>> scotland_cube = scotland.cube([occupation, region, continent], table=people)
    >>> scotland_cube.to_df()
                                               People
    Occupation    Region          Continent
    Manual Worker North           Australasia       0
                                  Europe            0
                                  Americas          0
                                  Asia              0
                                  Africa            0
                                               ...
    Retired       Channel Islands Australasia       0
                                  Europe            0
                                  Americas          0
                                  Asia              0
                                  Africa            0

    [700 rows x 1 columns]

*(this cube is identical to the previous one)*

Adding different measures
=========================

The :meth:`cube` method has a `measures` argument,
which you can use to specify which measures appear on the cube.
If this is not set, the default `count` measure is used automatically.

To display a count for another table pass its :class:`Table` object
in the `measures` list::

    >>> dest_cube = bookings.cube([dest], measures=[bookings, people, households])
    >>> dest_cube.to_df()
                   Bookings  People  Households
    Destination
    Australia        282719  274857      194412
    New Zealand         879     870         862
    Denmark            1510    1497        1483
    France           524474  522932      359194
    Germany          461260  214163      212004
    Greece           112092  109564       93208
    Italy             36881   25958       25612
    Latvia              645     551         542
    Portugal          21632   21230       20723
    Sweden            25207   25175       24055
    Jamaica             179     178         175
    United States    561842  273879      195757
    Kuwait            23548   23388       22349
    Mongolia            154     154         151
    Mali                974     968         961
    Namibia            2349    2276        2232
    Senegal             981     777         766
    Sierra Leone       4787    4778        4677
    South Africa        956     954         945

*(if you want the original count as well,
you will now need to include that explicitly in the measures list)*

Each measure is returned as a separate column on the DataFrame.

You can also add variable statistics
which can be imported from the :mod:`apteco.statistics` module::

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

.. seealso::
    For more information on working with DataFrames with a MultiIndex,
    see the `user guide
    <https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html>`_
    in the official Pandas documentation.

That's the end of the tutorial!
Hopefully you're now equipped with the knowledge you need
to get started on building your own selections, data grids and cubes.
Check out the rest of the documentation for more guidance,
and if you have any questions don't hesitate to get in touch
with Apteco Support (support@apteco.com) who will be happy to help.
