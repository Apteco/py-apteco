**************
  Quickstart
**************

Requirements
============

* Python 3.6+
* Access to an installation of the Apteco API

The Apteco API (which also goes under the name **Orbit API**)
is part of the Apteco Orbit™ installation.
If you have access to Apteco Orbit™, you also have access to the Apteco API!
If you're not sure about this, contact whoever administers your Apteco software,
or get in touch with Apteco support (support@apteco.com).

Installation
============

You can install the package the usual way from PyPI using ``pip``:

.. code-block:: console

   python -m pip install apteco

Logging in
==========

Your login credentials are the same username and password
you would use to log in to Apteco Orbit™:

.. code-block:: python

    >>> from apteco import login
    >>> my_session = login("https://my-site.com/OrbitAPI", "my_data_view", "my_system", "jdoe")

You will be asked to enter your password in the terminal, which won't be echoed.
If Python is unable to ask for your password in this way,
it will provide a pop-up box instead.
This might appear in the background,
so check your taskbar for a new window if nothing seems to be happening.

If you don't want to enter your password every time,
there's also a :func:`login_with_password` function which takes your password
as a fifth argument:

.. code-block:: python

    >>> from apteco import login_with_password
    >>> my_session = login_with_password(
    ...     "https://my-site.com/OrbitAPI",
    ...     "my_data_view",
    ...     "my_system",
    ...     "jdoe",
    ...     "password",  # password is in plain sight in the code!
    ... )

Tables
======

Tables are accessed through the :attr:`tables` attribute on the :class:`Session` object.
You can retrieve a table using its name:

.. code-block:: python

    >>> bookings = my_session.tables["Bookings"]

:class:`Table` objects have properties for various metadata:

.. code-block:: python

    >>> print(
    ...     f"There are {bookings.total_records:,}"
    ...     f" {bookings.plural.lower()}"
    ...     f" in the system."
    ... )
    There are 2,130,081 bookings in the system.

Variables
=========

Variables are accessed through the :attr:`variables` attribute
on the :class:`Session` object.
You can retrieve a variable using its name or description:

.. code-block:: python

    >>> surname = my_session.variables["peSName"]  # name
    >>> cost = my_session.variables["Cost"]  # description

Each table also has a :attr:`variables` attribute
for accessing the variables on that table:

.. code-block:: python

    >>> destination = bookings.variables["Destination"]

For convenience you can access variables by indexing into the :class:`Table` itself:

.. code-block:: python

    >>> destination = bookings["Destination"]

:class:`Variable` objects have attributes with various metadata:

.. code-block:: python

    >>> cost.description
    'Cost'
    >>> destination.type
    'Selector'

Creating selections
===================

You can use the Python operators with :class:`Variable` objects to build selections
based on criteria and return a count:

.. code-block:: python

    >>> sweden = bookings["Destination"] == "29"
    >>> sweden.count()
    25207

You can specify multiple values using any *iterable*:

.. code-block:: python

    >>> people = my_session.tables["People"]
    >>> high_earners = people["Income"] == (f"{i:02}" for i in range(7, 12))
    >>> high_earners.count()
    7114

You can use other operators as well; for example, to exclude values:

.. code-block:: python

    >>> households = my_session.tables["Households"]
    >>> uk_only = households["Region"] != "14"  # 14 is Channel Islands
    >>> uk_only.count()
    741572

Or to allow a range of values:

.. code-block:: python

    >>> low_profit = bookings["Profit"] <= 25
    >>> low_profit.count()
    211328

.. code-block:: python

    >>> second_half_of_alphabet = people["Surname"] >= "N"
    >>> second_half_of_alphabet.count()
    410954

Date and DateTime variables use the built-in :mod:`datetime` module:

.. code-block:: python

    >>> from datetime import date, datetime
    >>> bookings_before_2019 = bookings["Booking Date"] <= date(2018, 12, 31)
    >>> bookings_before_2019.count()
    972439

You can take advantage of functionality available in other Python packages:

.. code-block:: python

    >>> from dateutil.relativedelta import relativedelta
    >>> under_30 = people["DOB"] >= date.today() - relativedelta(years=30)
    >>> under_30.count()
    207737

Combining selections
====================

You can use the ``&`` ``|`` operators to combine selection criteria:

.. code-block:: python

    >>> sweden = bookings["Destination"] == "29"
    >>> cost_at_least_2k = bookings["Cost"] >= 2000
    >>> expensive_sweden = sweden & cost_at_least_2k
    >>> expensive_sweden.count()
    632
    >>> student = people["Occupation"] == "4"
    >>> under_21 = people["DOB"] >= date.today() - relativedelta(years=21)
    >>> eligible_for_discount = student | under_21
    >>> eligible_for_discount.count()
    188364

The ``~`` operator negates a selection:

.. code-block:: python

    >>> pay_full_price = ~eligible_for_discount
    >>> pay_full_price.count()
    968189

You can join clauses from different tables and it will automatically handle
the required table changes:

.. code-block:: python

    >>> high_affordability = high_earners | cost_at_least_2k  # will resolve to people
    >>> high_affordability.count()
    56096
    >>> high_affordability.table_name
    'People'

The left-most clause determines the resolve table:

.. code-block:: python

    >>> female = people["Gender"] == "F"
    >>> usa = bookings["Destination"] == "38"
    >>> female.table_name
    'People'
    >>> usa.table_name
    'Bookings'
    >>> (female & usa).table_name
    'People'
    >>> (usa & female).table_name
    'Bookings'

You can manually set the resolve table using the ``*`` operator:

.. code-block:: python

    >>> bookings_by_under_21s = bookings * under_21
    >>> bookings_by_under_21s.count()
    135100
    >>> bookings_by_under_21s.table_name
    'Bookings'

Compound clauses follow Python operator precedence:

.. code-block:: python

    >>> student_or_young_female = student | female & under_21
    >>> student_or_young_female.count()
    166708
    >>> student_or_female_must_be_young = (student | female) & under_21
    >>> student_or_female_must_be_young.count()
    49225

Be especially careful where compound clauses involve table changes:

.. code-block:: python

    >>> women_to_sweden = female & sweden
    >>> women_to_sweden.count()  # selection on People table
    8674
    >>> audience_1 = bookings * (female & sweden)
    >>> audience_1.count()  # bookings by women who've been to sweden
    23553
    >>> audience_2 = (bookings * female) & sweden
    >>> audience_2.count()  # bookings made by a woman, with destination of sweden
    8687

Creating data grids
===================

You can create a data grid from a table:

.. code-block:: python

    >>> urn = bookings["Booking URN"]
    >>> dest = bookings["Destination"]
    >>> occupation = people["Occupation"]
    >>> town = households["Town"]
    >>> datagrid = bookings.datagrid([urn, dest, cost, occupation, town])

Convert it to a Pandas DataFrame:

.. code-block:: python

    >>> datagrid.to_df()
        Booking URN    Destination     Cost       Occupation        Town
    0      10001265         France  1392.35  Sales Executive    Aberdeen
    1      10001266         France   780.34  Sales Executive    Aberdeen
    2      10011532        Germany   181.68    Manual Worker      Alford
    3      10011533        Germany   300.67    Manual Worker      Alford
    4      10015830   Unclassified   228.70  Sales Executive     Macduff
    ..          ...            ...      ...              ...         ...
    995    10996176  United States   241.24     Professional  Glenrothes
    996    10996177         Greece   343.23          Manager  Glenrothes
    997    10996178  United States   636.22          Manager  Glenrothes
    998    10996179  United States   356.21          Manager  Glenrothes
    999    10996180  United States   438.20          Manager  Glenrothes

    [1000 rows x 5 columns]

You can use a base selection to filter the records:

.. code-block:: python

    >>> sweden = dest == "29"
    >>> sweden_datagrid = sweden.datagrid([urn, dest, cost, occupation, town])
    >>> sweden_datagrid.to_df()
        Booking URN Destination     Cost       Occupation           Town
    0      10172319      Sweden  1201.81  Sales Executive         Bolton
    1      10384970      Sweden   344.30          Manager     Chelmsford
    2      10421011      Sweden   322.89  Sales Executive        Croydon
    3      10425298      Sweden   880.02          Student  South Croydon
    4      10479109      Sweden   172.91    Retail Worker       Nantwich
    ..          ...         ...      ...              ...            ...
    995    11471824      Sweden   118.76  Sales Executive    King's Lynn
    996    11576762      Sweden   652.38    Public Sector        Redhill
    997    11576764      Sweden   183.36    Public Sector        Redhill
    998    11682962      Sweden  1166.38          Manager         London
    999    11754655      Sweden   192.45  Sales Executive          Ascot

    [1000 rows x 5 columns]

You can filter using a selection from a different table:

.. code-block:: python

    >>> manchester = households["Region"] == "13"
    >>> manc_datagrid = manchester.datagrid(
    ...     [urn, dest, cost, occupation, town], table=bookings
    ... )
    >>> manc_datagrid.to_df()
        Booking URN    Destination     Cost       Occupation         Town
    0      10172319         Sweden  1201.81  Sales Executive       Bolton
    1      10172320  United States  1616.80  Sales Executive       Bolton
    2      10173729         France   581.71          Student       Bolton
    3      10173730         France  2224.70          Student       Bolton
    4      10177047         France   686.53  Sales Executive       Bolton
    ..          ...            ...      ...              ...          ...
    995    11739340      Australia   316.60     Professional  Stalybridge
    996    11739342   Unclassified   316.58  Sales Executive  Stalybridge
    997    12087034         Greece  1305.66    Public Sector   Altrincham
    998    12087035  United States   585.65    Public Sector   Altrincham
    999    12087036      Australia   496.64    Public Sector   Altrincham

    [1000 rows x 5 columns]

Creating cubes
==============

You can create a cube from a table:

.. code-block:: python

    >>> occupation = people["Occupation"]
    >>> income = people["Income"]
    >>> gender = people["Gender"]
    >>> cube = people.cube([occupation, income, gender])

Convert it to a Pandas DataFrame:

.. code-block:: python

    >>> df = cube.to_df()
    >>> df.head(10)
                                   People
    Occupation    Income  Gender
    Manual Worker <£10k   Female    15624
                          Male       5321
                          Unknown       5
                  £10-20k Female    43051
                          Male       5992
                          Unknown      25
                  £20-30k Female     1498
                          Male        649
                          Unknown      14
                  £30-40k Female      675

You can pivot the dimensions to make it easier to read:

.. code-block:: python

    >>> df.unstack(level=0)
                       People          ...
    Occupation       Director Manager  ... Student Unemployed
    Income   Gender                    ...
    <£10k    Female      1279    4649  ...   28002      21385
             Male         832    2926  ...   14296       8386
             Unknown        4      16  ...      10        155
    £10-20k  Female      4116   16665  ...   39462      17230
             Male        2139    9123  ...   17917       4532
             Unknown        9      47  ...      25        368
    £100k+   Female         2       1  ...       2          0
             Male           1       0  ...       3          0
             Unknown        1       0  ...       1          0
    £20-30k  Female      1267    6238  ...    6669       5747
             Male        1050    5315  ...    5274       1345
             Unknown        5      45  ...      22        236
    £30-40k  Female      1591    6621  ...    5690       3117
             Male        1940    9713  ...    6345       1049
             Unknown       46     140  ...      63        519
    £40-50k  Female       265     965  ...     587        262
             Male         518    1800  ...     943        115
             Unknown       22      58  ...      29        110
    £50-60k  Female       336     806  ...     425        277
             Male         607    1677  ...     692         69
             Unknown       47      88  ...      64         89
    £60-70k  Female        40     112  ...      54         58
             Male          96     220  ...      95          8
             Unknown       11      16  ...      17         17
    £70-80k  Female        44      96  ...      42         27
             Male         102     179  ...      63          5
             Unknown       12      22  ...      15          5
    £80-90k  Female        11      11  ...       3          0
             Male          14      13  ...      16          0
             Unknown        4       3  ...       5          0
    £90-100k Female         1       0  ...       1          1
             Male          11       7  ...       4          0
             Unknown        3       6  ...       9          0

    [33 rows x 10 columns]

You can use a base selection to filter the records:

.. code-block:: python

    >>> occupation = people["Occupation"]
    >>> region = households["Region"]
    >>> student = occupation == "4"
    >>> student_cube = student.cube([occupation, dest, region])
    >>> student_df = student_cube.to_df()
    >>> student_df.head()
                                                                     People
    Occupation    Destination Region
    Manual Worker Australia   North                                       0
                              North West (Excluding Gtr Manchester)       0
                              South East (Outside M25 )                   0
                              South West                                  0
                              East Midlands                               0

Selecting only cells where ``Occupation`` is *Student*,
and pivoting ``Destination`` dimension:

.. code-block:: python

    >>> student_df.loc["Student"].unstack(level=0)
                                             People          ...
    Destination                           Australia Denmark  ... Sweden United States
    Region                                                   ...
    Channel Islands                              46       1  ...     10            81
    East Anglia                                 989       0  ...    109           905
    East Midlands                              1956       0  ...    174          1762
    Greater Manchester                         1197       1  ...    147          1089
    North                                       959       2  ...    115           869
    North West (Excluding Gtr Manchester)      1594       2  ...    177          1429
    Northern Ireland                            467       0  ...     42           492
    Scotland                                   2061       1  ...    224          1964
    South East (Inside M25 )                   3935       0  ...    390          3580
    South East (Outside M25 )                  6255       1  ...    608          5587
    South West                                 2310       0  ...    182          2037
    Wales                                       974       0  ...    122           860
    West Midlands                              2643       0  ...    288          2362
    Yorkshire and Humber                       2295       0  ...    249          2089

    [14 rows x 19 columns]

You can use a selection from a different table to filter the records in the cube:

.. code-block:: python

    >>> manchester = region == "13"
    >>> manc_cube = manchester.cube([occupation, dest, region], table=bookings)
    >>> manc_cube.to_df()
                                                                      Bookings
    Occupation    Destination  Region
    Manual Worker Australia    North                                         0
                               North West (Excluding Gtr Manchester)         0
                               South East (Outside M25 )                     0
                               South West                                    0
                               East Midlands                                 0
                                                                        ...
    Retired       South Africa Scotland                                      0
                               Wales                                         0
                               Northern Ireland                              0
                               Greater Manchester                            0
                               Channel Islands                               0

    [2660 rows x 1 columns]

For a more thorough introduction, check out the :ref:`tutorial`.
