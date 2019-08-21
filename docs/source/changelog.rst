Change Log
==========

Version 0.1.2
-------------

Fixed
^^^^^

* Not able to connect to a different API host after first connection
  during any single Python session.

Version 0.1.1
-------------

Fixed
^^^^^

* ``.isin()`` method on variables not passing on variable object correctly.

Version 0.1.0
-------------

Added
^^^^^

* Log in to the API and create a session which has tables and variables data.
* Build selections with the following types of clauses:

  - Selector
  - Combined categories
  - Numeric
  - Text
  - Array
  - Flag array
  - Boolean (``AND``, ``OR``, ``NOT``)
  - Table (``ANY``, ``THE``)
  - Subselection

* Specify selected values using ``str`` literals.
* Return a count for the final selection.
