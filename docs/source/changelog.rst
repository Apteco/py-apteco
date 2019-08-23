Change Log
==========

Version 0.2.0
-------------

*2019-08-23*

Added
^^^^^
* Added ``serialize()`` and ``deserialize()`` methods to the ``Session`` class.
* Added documentation (Getting Started guide and Change Log).

Version 0.1.2
-------------

*2019-08-05*

Fixed
^^^^^

* Fixed not being able to connect to a different API host after first connection
  during any single Python session.

Version 0.1.1
-------------

*2019-08-05*

Fixed
^^^^^

* Fixed ``isin()`` method on variables not working.

Version 0.1.0
-------------

*2019-07-05*

Added
^^^^^

* Added ``login()`` and ``login_with_password()`` functions to log in to the API.
* Added ``Session`` class for creating an API session.
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
