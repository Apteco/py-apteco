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
    >>> dg = bookings.datagrid([urn, dest, cost, occupation, town])

Convert it to a Pandas DataFrame:

.. code-block:: python

    >>> dg.to_df()
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
    >>> sweden_dg = sweden.datagrid([urn, dest, cost, occupation, town])
    >>> sweden_dg.to_df()
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
    >>> manc_dg = manchester.datagrid(
    ...     [urn, dest, cost, occupation, town], table=bookings
    ... )
    >>> manc_dg.to_df()
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

    >>> dest = bookings["Destination"]
    >>> product = bookings["Product"]
    >>> grade = bookings["Grade"]
    >>> cube = bookings.cube([dest, product, grade])

Convert it to a Pandas DataFrame:

.. code-block:: python

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

You can pivot the dimensions to make it easier to read:

.. code-block:: python

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

You can use a base selection to filter the records

.. code-block:: python

    >>> occupation = people["Occupation"]
    >>> region = households["Region"]
    >>> sweden = dest == "29"
    >>> sweden_cube = sweden.cube([dest, occupation, region])
    >>> sweden_df = sweden_cube.to_df()
    >>> sweden_df.head()
                                                                     Bookings
    Destination  Occupation   Region
    Unclassified Unclassified Unclassified                                  0
                              North                                         0
                              North West (Excluding Gtr Manchester)         0
                              South East (Outside M25 )                     0
                              South West                                    0

Selecting only cells where ``Destination`` is *Sweden*,
and pivoting ``Occupation`` dimension:

.. code-block:: python

    >>> sweden_df.loc["Sweden"].unstack(level=0)
                                          Bookings          ...
    Occupation                            Director Manager  ... Unclassified Unemployed
    Region                                                  ...
    Channel Islands                              0       6  ...            0          0
    East Anglia                                 35     133  ...            6         16
    East Midlands                              126     332  ...            3         22
    Greater Manchester                          77     226  ...            1         18
    North                                       26     129  ...            0         10
    North West (Excluding Gtr Manchester)       71     269  ...            4         25
    Northern Ireland                            35      40  ...            1          8
    Scotland                                    79     165  ...            2         19
    South East (Inside M25 )                   125     448  ...           13         60
    South East (Outside M25 )                   88     747  ...            2         59
    South West                                  46     245  ...            2         28
    TOTAL                                      905    3902  ...           43        324
    Unclassified                                 4      45  ...            0          1
    Wales                                       28     146  ...            2          9
    West Midlands                               67     589  ...            3         29
    Yorkshire and Humber                        98     382  ...            4         20

    [16 rows x 12 columns]

You can use a selection from a different table to filter the records in the cube:

.. code-block:: python

    >>> manchester = region == "13"
    >>> manc_cube = manchester.cube([dest, occupation, region], table=bookings)
    >>> manc_cube.to_df()
                                                                         Bookings
    Destination  Occupation   Region
    Unclassified Unclassified Unclassified                                  0
                              North                                         0
                              North West (Excluding Gtr Manchester)         0
                              South East (Outside M25 )                     0
                              South West                                    0
                                                                       ...
    TOTAL        TOTAL        Wales                                         0
                              Northern Ireland                              0
                              Greater Manchester                        81812
                              Channel Islands                               0
                              TOTAL                                     81812

    [4032 rows x 1 columns]

For a more thorough introduction, check out the :ref:`tutorial`.
