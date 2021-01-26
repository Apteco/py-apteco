**************
  Change Log
**************

Version 0.7.0
=============

*2021-01-26*

Added
-----

* Added ``LimitClause``, ``TopNClause``, ``NPerVariableClause``, ``NPerTableClause``
  classes for creating selections with limits.
* Added ``sample()`` and ``limit()`` methods to selections for applying limits to them.
* Added cube variable statistics in new ``apteco.statistics`` module:

  - ``Sum``
  - ``Mean``
  - ``Populated``
  - ``Min``
  - ``Max``
  - ``Median``
  - ``Mode``
  - ``Variance``
  - ``StdDev``
  - ``LowerQuartile``
  - ``UpperQuartile``
  - ``InterQuartileRange``
  - ``CountDistinct``
  - ``CountMode``

* Added ``missing()`` method to ``NumericVariable`` for selecting records
  with missing values.

Changed
-------

* Cubes can now have multiple measures rather than just the single default count.
* For cubes with just a single dimension, ``Cube.to_df()`` now returns a DataFrame
  with a normal ``Index`` (rather than a ``MultiIndex``).

Deprecated
----------

* ``NumericVariable.max`` → use ``NumericVariable.max_value``
* ``NumericVariable.min`` → use ``NumericVariable.min_value``

Fixed
-----

* Process that validates cube dimensions and measures has been improved
  to catch some invalid combinations that were previously allowed,
  and allow some valid combinations that were previously prevented.


Version 0.6.0
=============

*2020-10-22*

Added
-----

* Added ability to pick variables by description.
* Added ``table_name`` property to ``Variable`` classes (alias of ``table.name``).
* Added ``is_related()`` method to ``Table``.
* Added ``allow_same`` keyword to ``is_ancestor()``, ``is_descendant()``
  & ``is_related()`` methods on ``Table``.
* Added ``<=`` and ``>=`` operators to ``Table``
  corresponding to these ``is_ancestor(allow_same=True)``
  and ``is_descendant(allow_same=True)``.
* Added methods to ``TextVariable``
  to enable querying text variables with different text match types:

  - ``equals()``
  - ``contains()``
  - ``startswith()``
  - ``endswith()``
  - ``between()``
  - ``matches()``

* Added ``datagrid()`` and ``cube()`` methods to tables and selections
  to enable building Data Grids and Cubes directly from these.
* Added ``AptecoDeprecationWarning`` for warning about deprecated features.

Changed
-------

* Simplified some ``Table`` attribute names
  (the old names still work but issue an ``AptecoDeprecationWarning``):

  - ``singular_display_name`` -> ``singular``
  - ``plural_display_name`` -> ``plural``
  - ``is_default_table`` -> ``is_default``
  - ``is_people_table`` -> ``is_people``
  - ``child_relationship_name`` -> ``child_relationship``
  - ``parent_relationship_name`` -> ``parent_relationship``
  - ``has_child_tables`` -> ``has_children``

* ``Session.tables`` is now a ``TablesAccessor`` object instead of ``dict``:

  - can pick tables by name using ``[]`` (as before)
  - can use ``for ... in`` to loop over tables
  - can use ``len()`` to get the number of tables

* ``Session.variables`` and ``Table.variables``
  is now a ``VariablesAccessor`` object instead of ``dict``:

  - can pick variables by name or description using ``[]``
    (as before for names; support for descriptions is new)
  - can use ``for ... in`` to loop over variables
  - can use ``len()`` to get the number of variables (in the system or on the table)
  - has ``names`` attribute for picking by name-only (using ``[]``)
    and looping over variable names (using ``for ... in``)
  - has ``descs`` attribute for picking by description-only (using ``[]``)
    and looping over variable descriptions (using ``for ... in``)
  - has ``descriptions`` attribute, which is alias of ``descs``

* The columns on the ``DataFrame`` returned by ``DataGrid.to_df()``
  now have the data type that matches the FastStats variable for that column.
* Variables from ancestor tables can now be used as columns on a ``DataGrid``.
* Variables from related tables can now be used as dimensions on a ``Cube``.

Removed
-------

* Removed ``isin()`` and ``contains()`` method from ``Variable`` base class completely
  (had been previously deprecated to raise ``NotImplementedError``).
  ``contains()`` has been implemented on ``TextVariable``
  and it is planned to implement these methods for applicable variable types in future.

Fixed
-----

* During variables initialisation process,
  variables with unrecognised type now log a warning rather than raising exception
  (this means program execution can continue rather than stopping completely).
* It is now possible to change the table of a selection
  to a table that is not a direct ancestor or descendant
  (this previously raised an ``OperationError``).

Version 0.5.0
=============

*2020-06-03*

Added
-----

* Added ``DataGrid`` class for creating Data Grids (export of FastStats data).
* Added ``Cube`` class for creating Cubes (summary of FastStats data).
* Added ``to_df()`` method to ``DataGrid`` and ``Cube`` classes
  for converting these objects to a Pandas ``DataFrame``.

Changed
-------

* You can now import ``login``, ``login_with_password`` and ``Session``,
  along with the new ``DataGrid`` and ``Cube``, directly from the ``apteco`` package.

Removed
-------

* Removed ``select()`` method from ``Table`` and ``Clause`` classes
  and ``select()`` function from query module,
  as this was not publicly documented and the direct ``count()`` method is preferred
  over ``select().count``.
  It was wanted to reserve the ``select`` name for other potential future functionality.

Version 0.4.0
=============

*2020-04-07*

Added
-----

* Added the ability to build selections using the
  ``==``, ``!=``, ``<``, ``>``, ``<=``, ``>=`` comparison operators with
  **Selector**, **Numeric**, **Text**, **Array**, **FlagArray**, **Date**, **DateTime**
  variables, and value(s) of the matching object type,
  e.g. ``DateVariable`` with a Python ``datetime.date`` object.
  (Note: not all FastStats variable types support all comparison operators.)
* Added ``DateRangeClause``, ``TimeRangeClause``, ``DateTimeRangeClause`` classes
  for creating selection clauses.
* Added ``is_ancestor()``, ``is_descendant()``, ``is_same()`` methods
  to ``Table`` class for checking table relationships.
* Added ``count()`` method to ``Table`` class to enable direct counting
  of empty query comprising just a table.
* Added ``system_info`` attribute to ``Session`` class which returns
  FastStats system metadata as a ``namedtuple``.
* Added installation guide, tutorial,
  and reference guides for ``Session`` and ``Variable`` objects.
* Added keywords and classifiers to project (for PyPI).
* Added continuous integration using Azure Pipelines
  so tests now run automatically during development process.
  This includes measuring test coverage.

Changed
-------

* ``login()`` and ``login_with_password()`` functions now return ``Session`` object
  directly, instead of an intermediary ``Credentials`` object.
* The variables dictionaries on ``Session`` and ``Table`` objects
  now have variable *names* as keys, instead of *descriptions*.
* ``Variable`` classes now have ``table`` attribute
  which returns the ``Table`` object for the table they belong to.
* ``CriteriaClause`` classes no longer have ``table`` parameter in signature;
  their ``table`` attribute is derived from ``variable``.
* The comparison operators on tables are now reversed so that
  ``[ancestor table] < [descendant table]`` is true.
  This is to fit with the idea of the master table as the 'root' table
  and ancestor tables as having greater precedence to child and descendant tables.
* The ``user`` attribute on ``Session`` is now a ``namedtuple``
  rather than its own ``User`` class.
* If the master table can't be found during session initialization,
  it now gives more specific error messages about what went wrong.
* If table relations aren't initialized correctly,
  it now tells you about all the cases that fail, not just the first one it finds.

Removed
-------

* Removed ``CombinedCategoriesVariable`` class,
  as its implementation didn't cover all types of Combined Categories variables.
  Variables of this type have reverted to the more general ``SelectorVariable``.
  It is planned to re-implement Combined Categories variable support in future.
* Removed ``isin()`` method on variables, as it's not applicable to all variable types.
  It is planned to re-implement this method for relevant variables in future.

Fixed
-----

* Session initialization process now loads all system tables,
  not just the first 10.
* Using generators to return selector codes
  for building selections (with ``==`` operator) now works.

Version 0.3.2
=============

*2019-10-01*

Fixed
-----

* Improved code syntax highlighting in the README.


Version 0.3.1
=============

*2019-10-01*

Fixed
-----

* Set Getting Started guide as the README.


Version 0.3.0
=============

*2019-10-01*

Added
-----

* Added ``DateListClause`` for creating selections with list of dates.
* Added ``select()`` method to ``Tables`` class to enable counting empty queries.

Changed
-------

* Each variable type now has a specific class with only the attributes pertinent to it.


Version 0.2.0
=============

*2019-08-23*

Added
-----

* Added ``serialize()`` and ``deserialize()`` methods to the ``Session`` class.
* Added documentation (Getting Started guide and Change Log).


Version 0.1.2
=============

*2019-08-05*

Fixed
-----

* Fixed not being able to connect to a different API host after first connection
  during any single Python session.


Version 0.1.1
=============

*2019-08-05*

Fixed
-----

* Fixed ``isin()`` method on variables not working.


Version 0.1.0
=============

*2019-07-05*

Added
-----

* Added ``login()`` and ``login_with_password()`` functions to log in to the API.
* Added ``Session`` class for creating an API session.
* Added ``Table`` class representing FastStats system tables.
* Added support for accessing variables on a table using the ``[]`` operator
  with the variable description.
* Added support for testing equality of tables using the ``==`` operator.
* Added support for testing if a table is an ancestor or descendant of another
  using the ``>`` and ``<`` operators (respectively).
* Added ``SelectorClause``, ``CombinedCategoriesClause``, ``NumericClause``,
  ``TextClause``, ``ArrayClause``, ``FlagArrayClause`` classes
  for creating selection clauses.
* Added support for creating selection clauses using the ``==`` operator on variables
  with ``str`` literals to set values.
* Added ``isin()`` method on variables to select values using an iterable.
* Added ``BooleanClause`` class to apply boolean logic to clauses
  (``AND``, ``OR``, ``NOT``).
* Added support for applying boolean logic using the ``&``, ``|``, ``~`` operators
  on clauses.
* Added ``TableClause`` class for changing resolve table level of clauses
  (``ANY``, ``THE``).
* Added support for using the ``*`` operator with a clause and a table
  to change the resolve table of the clause.
* Added ``SubSelectionClause`` class for using a subselection in a selection.
* Added ``Selection`` class for creating a selection from a query,
  with ``get_count()`` and ``set_table()`` methods.
* Added ``select()`` method on clauses to create a ``Selection`` from the clause.
* Added ``select()`` function for creating a selection using a clause.
