**************
  apteco-api
**************

The ``apteco-api`` package is a thin wrapper around the Apteco API
and provides a Python interface to the API, replacing HTTP requests using JSON
with Python method calls using Python objects.

It is auto-generated from the Apteco API spec using the OpenAPI generator:

    * Each group in the API becomes a class,
      e.g. the *Queries* group becomes a class called ``QueriesApi``
    * Each endpoint within that group becomes a method on that group's class,
      e.g. the *CountSync* endpoint becomes the
      ``queries_perform_query_count_synchronously`` method on the ``QueriesApi`` class.
    * Parameters (whether path, query or body parameters) become method arguments,
      e.g. `systemName` (a path parameter), `query` (a body parameter)
      and `returnDefinition` (a query parameter)
      become the ``system_name``, ``query`` and ``return_definition`` arguments in the
      ``queries_perform_query_count_synchronously`` method.
    * Each model in the API becomes a Python class, and JSON model objects that are
      either passed as parameters in a request to an endpoint
      or returned in the result become Python objects,
      e.g. the ``query`` argument in the ``queries_perform_query_count-synchronously``
      method call takes in instance of the ``Query`` class,
      and the method returns an instance of the ``QueryResult`` class.

.. toctree::
    :caption: Further reference
    :maxdepth: 1

    apteco-api/changelog_apteco_api.rst
