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

If we don't specify any measures, the `count` measure is used by default.

To work with the data we can convert it to a Pandas :class:`DataFrame`
using the :meth:`to_df()` method::

    >>> df = cube.to_df()
    >>> df
                                  People
    Income Occupation    Gender
    <£10k  Manual Worker Female    15624
                         Male       5321
                         Unknown       5
           Director      Female     1279
                         Male        832
                                  ...
    £100k+ Unemployed    Male          0
                         Unknown       0
           Retired       Female        0
                         Male          1
                         Unknown       0

    [330 rows x 1 columns]

The DataFrame uses a `MultiIndex
<https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.MultiIndex.html>`_,
with each dimension as a different level in the index::

    >>> df.index
    MultiIndex([( '<£10k', 'Manual Worker',  'Female'),
            ( '<£10k', 'Manual Worker',    'Male'),
            ( '<£10k', 'Manual Worker', 'Unknown'),
            ( '<£10k',      'Director',  'Female'),
            ( '<£10k',      'Director',    'Male'),
            ( '<£10k',      'Director', 'Unknown'),
            ( '<£10k',       'Manager',  'Female'),
            ( '<£10k',       'Manager',    'Male'),
            ( '<£10k',       'Manager', 'Unknown'),
            ( '<£10k',  'Professional',  'Female'),
            ...
            ('£100k+', 'Retail Worker', 'Unknown'),
            ('£100k+', 'Public Sector',  'Female'),
            ('£100k+', 'Public Sector',    'Male'),
            ('£100k+', 'Public Sector', 'Unknown'),
            ('£100k+',    'Unemployed',  'Female'),
            ('£100k+',    'Unemployed',    'Male'),
            ('£100k+',    'Unemployed', 'Unknown'),
            ('£100k+',       'Retired',  'Female'),
            ('£100k+',       'Retired',    'Male'),
            ('£100k+',       'Retired', 'Unknown')],
           names=['Income', 'Occupation', 'Gender'], length=330)

The DataFrame has one column which is the single default count measure,
named after the resolve table of the cube,
which corresponds to the entity it is counting.
Since the data values represent a count, they are all integers::

    >>> df.info()
    <class 'pandas.core.frame.DataFrame'>
    MultiIndex: 330 entries, ('<£10k', 'Manual Worker', 'Female') to ('£100k+', 'Retired', 'Unknown')
    Data columns (total 1 columns):
     #   Column  Non-Null Count  Dtype
    ---  ------  --------------  -----
     0   People  330 non-null    int64
    dtypes: int64(1)
    memory usage: 4.6+ KB

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
    Gender                   Female   Male Unknown
    Income   Occupation
    <£10k    Director          1279    832       4
             Manager           4649   2926      16
             Manual Worker    15624   5321       5
             Professional      2316   1388       7
             Public Sector    29593  20278     247
                             ...    ...     ...
    £90-100k Retail Worker       31     51     118
             Retired              0      2       0
             Sales Executive     15     32      14
             Student              1      4       9
             Unemployed           1      0       0

    [110 rows x 3 columns]

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

*(this data grid is identical to the previous one)*

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
