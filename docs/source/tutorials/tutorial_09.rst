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

    >>> income = people["Income"]
    >>> occupation = people["Occupation"]
    >>> gender = people["Gender"]
    >>> cube = people.cube([income, occupation, gender])

Only the default `count` measure is currently supported,
and this is included in the cube automatically.

To work with the data we can convert it to a Pandas :class:`DataFrame`
using the :meth:`to_df()` method::

    >>> df = cube.to_df()
    >>> df
                                             People
    Income       Occupation   Gender
    Unclassified Unclassified Unclassified        0
                              Female              0
                              Male                0
                              Unknown             0
                              TOTAL               0
                                             ...
    TOTAL        TOTAL        Unclassified        0
                              Female         764796
                              Male           378567
                              Unknown         13190

                              TOTAL         1156553

    [780 rows x 1 columns]

The DataFrame uses a `MultiIndex
<https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.MultiIndex.html>`_,
with each dimension as a different level in the index::

    >>> df.index
    MultiIndex([('Unclassified',  'Unclassified', 'Unclassified'),
                ('Unclassified',  'Unclassified',       'Female'),
                ('Unclassified',  'Unclassified',         'Male'),
                ('Unclassified',  'Unclassified',      'Unknown'),
                ('Unclassified',  'Unclassified',        'TOTAL'),
                ('Unclassified', 'Manual Worker', 'Unclassified'),
                ('Unclassified', 'Manual Worker',       'Female'),
                ('Unclassified', 'Manual Worker',         'Male'),
                ('Unclassified', 'Manual Worker',      'Unknown'),
                ('Unclassified', 'Manual Worker',        'TOTAL'),
                ...
                (       'TOTAL',       'Retired', 'Unclassified'),
                (       'TOTAL',       'Retired',       'Female'),
                (       'TOTAL',       'Retired',         'Male'),
                (       'TOTAL',       'Retired',      'Unknown'),
                (       'TOTAL',       'Retired',        'TOTAL'),
                (       'TOTAL',         'TOTAL', 'Unclassified'),
                (       'TOTAL',         'TOTAL',       'Female'),
                (       'TOTAL',         'TOTAL',         'Male'),
                (       'TOTAL',         'TOTAL',      'Unknown'),
                (       'TOTAL',         'TOTAL',        'TOTAL')],
               names=['Income', 'Occupation', 'Gender'], length=780)

The DataFrame has one column which is the single default count measure,
named after the resolve table of the cube,
which corresponds to the entity it is counting.
Since the data values represent a count, they are all integers::

    >>> df.info()
    <class 'pandas.core.frame.DataFrame'>
    MultiIndex: 780 entries, ('Unclassified', 'Unclassified', 'Unclassified') to ('TOTAL', 'TOTAL', 'TOTAL')
    Data columns (total 1 columns):
     #   Column  Non-Null Count  Dtype
    ---  ------  --------------  -----
     0   People  780 non-null    int32
    dtypes: int32(1)
    memory usage: 6.8+ KB

.. tip::
    This initial structure of the DataFrame returned by the :meth:`to_df()` method
    is very similar to a *Tree* in the FastStats application.
    However, the cube also includes subtotals which a tree doesn't.

Pivoting the ``Gender`` dimension returns a :class:`DataFrame`
with ``Gender`` as a new level of column labels.
You may find this arrangement easier to read
and more similar to how a cube would be presented in FastStats::

    >>> df.unstack(level=2)
                             People
    Gender                   Female   Male  TOTAL Unclassified Unknown
    Income   Occupation
    <£10k    Director          1279    832   2115            0       4
             Manager           4649   2926   7591            0      16
             Manual Worker    15624   5321  20950            0       5
             Professional      2316   1388   3711            0       7
             Public Sector    29593  20278  50118            0     247
                             ...    ...    ...          ...     ...
    £90-100k Sales Executive     15     32     61            0      14
             Student              1      4     14            0       9
             TOTAL               75    145    415            0     195
             Unclassified         0      0      0            0       0
             Unemployed           1      0      1            0       0

    [156 rows x 5 columns]

Only Selector variables are currently supported as cube dimensions,
and this doesn't include Selector subtypes such as
Array, Flag Array, Date or Datetime.
As in FastStats, you can also use variables from 'related' tables,
that is, ancestor or descendant tables (including the direct parent and children)::

    >>> region = households["Region"]
    >>> continent = bookings["Continent"]
    >>> mixed_tables_cube = people.cube([region, occupation, continent])
    >>> mixed_tables_cube.to_df()
                                             People
    Region       Occupation   Continent
    Unclassified Unclassified Unclassified        0
                              Australasia         6
                              Europe              7
                              Americas            4
                              Asia                0
                                             ...
    TOTAL        TOTAL        Europe         895009
                              Americas       274023
                              Asia            23481
                              Africa           9298
                              TOTAL         1156553

    [1344 rows x 1 columns]

.. note::
    This is the table structure for the tables
    from the demo *Holidays* system being used here::

        Households
         └─ People
             └─ Bookings

    Our cube is showing a count of `People` records, but the dimensions include
    the `Region` variable from the parent `Households` table,
    as well as the `Continent` variable from the child `Bookings` table.

Applying a selection
====================

You can filter the records used in the analysis for the cube
by applying a selection to it using the `selection` parameter::

    >>> student = people["Occupation"] == "4"
    >>> student_cube = people.cube([occupation, region, continent], selection=student)
    >>> student_cube.to_df()
                                            People
    Region       Occupation   Continent
    Unclassified Unclassified Unclassified       0
                              Australasia        0
                              Europe             0
                              Americas           0
                              Asia               0
                                            ...
    TOTAL        TOTAL        Europe        105374
                              Americas       25371
                              Asia            1914
                              Africa           685
                              TOTAL         126845

    [1344 rows x 1 columns]

You can also build the cube directly
from the selection using the :meth:`cube` method::

    >>> student_cube = student.cube([occupation, region, continent])
    >>> student_cube.to_df()
                                            People
    Occupation   Region       Continent
    Unclassified Unclassified Unclassified       0
                              Australasia        0
                              Europe             0
                              Americas           0
                              Asia               0
                                            ...
    TOTAL        TOTAL        Europe        105374
                              Americas       25371
                              Asia            1914
                              Africa           685
                              TOTAL         126845

    [1344 rows x 1 columns]

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
    Occupation   Region       Continent
    Unclassified Unclassified Unclassified       0
                              Australasia        0
                              Europe             0
                              Americas           0
                              Asia               0
                                            ...
    TOTAL        TOTAL        Europe         69569
                              Americas       17305
                              Asia            1538
                              Africa           506
                              TOTAL          86985

    [1344 rows x 1 columns]

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
    Occupation   Region       Continent
    Unclassified Unclassified Unclassified       0
                              Australasia        0
                              Europe             0
                              Americas           0
                              Asia               0
                                            ...
    TOTAL        TOTAL        Europe         69569
                              Americas       17305
                              Asia            1538
                              Africa           506
                              TOTAL          86985

    [1344 rows x 1 columns]

*(this data grid is identical to the previous one)*

.. seealso::
    For more information on working with DataFrames with a MultiIndex,
    see the `user guide
    <https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html>`_
    in the official Pandas documentation.
