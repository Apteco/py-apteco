=============================
Change Log for ``apteco-api``
=============================

A record of changes to the ``apteco-api`` package
which are, or may be, relevant to **py-apteco**.
Since the ``apteco-api`` package is auto-generated from the **OrbitAPI** spec,
these changes correspond directly to changes there.

Version 0.2.0
-------------

**25 Oct 2019**

* apteco-api commit: ``703a653``
* OrbitAPI version: ``1.8.13.2139``
* OrbitAPI date: 25 Oct 2019

Added
^^^^^

* ``/{dataViewName}/Exports``
* ``/{dataViewName}/Exports/{systemName}``
* ``/{dataViewName}/Queries/{systemName}/SaveFileSync``

Changed
^^^^^^^

* ``Selection``, ``Logic``, ``Criteria``:
    - ``tableName`` now required
* ``FastStatsSystemSummary``, ``FastStatsSystemDetail``:
    - ``velocityType`` removed



Version 0.1.10
--------------

**19 Oct 2019**

* apteco-api commit: ``3c8c303``
* OrbitAPI version: ``1.8.12.1960``
* OrbitAPI date: 12 Oct 2019

Added
^^^^^

* ``NumericVariableInfo``
    - ``currencySymbol`` property
* ``Dimension``
    - ``filterQuery`` property
* ``FastStatsSystemSummary``, ``FastStatsSystemDetail``
    - ``velocityType`` property


Version 0.1.9
--------------

**01 Oct 2019**

* apteco-api commit: ``a107ed5``
* (OrbitAPI version: ``1.8.11.1775``)
* (OrbitAPI date: 27 Sep 2019)

*(Spec unchanged: only version number changed.)*


Version 0.1.8
--------------

**01 Oct 2019**

* apteco-api commit: ``008a8c7``
* (OrbitAPI version: ``1.8.11.1775``)
* (OrbitAPI date: 27 Sep 2019)

Fixed
^^^^^

* ``/{dataViewName}/Telemetry/States/ForUser/{username}`` **GET**
    - Corrected capitalisation of ``username`` (previously ``Username``)
    - Spec incorrect - did not match API behaviour


Version 0.1.7
--------------

**30 Sep 2019**

* apteco-api commit: ``9634c69``
* OrbitAPI version: ``1.8.11.1775``
* OrbitAPI date: 27 Sep 2019

Added
^^^^^

* ``/{dataViewName}/Sessions/TokenLogin``  **POST**
* ``/{dataViewName}/Settings/DataView`` **GET** **PUT** **DELETE**
* ``/{dataViewName}/Settings/DataView/{settingsPath}`` **GET** **PUT** **DELETE**
* ``/{dataViewName}/Users/{username}/LoginHistory`` **GET**
* ``SelectorVariableInfo``
    - ``combinedFromVariableName`` property
* ``SessionDetails``
    - ``lastLogin`` property
* ``TokenLoginDetails``
* ``PagedResults[UserLogin]``
* ``UserLogin``

Changed
^^^^^^^

* ``/{dataViewName}/Cubes/{systemName}/CalculateSync`` **POST**, ``/{dataViewName}/Exports/{systemName}/ExportSync`` **POST**, ``/{dataViewName}/Queries/{systemName}/CountSync`` **POST**, ``/{dataViewName}/Queries/{systemName}/CountFileSync`` **POST**
    - ``returnDefinition`` defaults to false
* ``CubeResult``
    - No longer requires any properties (previously required ``ranSuccessfully``, ``dimensionResults``, ``measureResults``)
* ``ExportResult``
    - No longer requires any properties (previously required ``ranSuccessfully``)
* ``SessionDetails``
    - ``lastLogin`` property now required (in addition to ``accessToken``, ``user``, ``sessionId``, ``license``)

Removed
^^^^^^^

* ``PagedResults[FastStatsSystemDetail]``


Version 0.1.6
--------------

**08 Aug 2019**

* apteco-api commit: ``dd9f998``
* (OrbitAPI version: ``1.8.3.915``)
* (OrbitAPI date: 21 Jun 2019)

Fixed
^^^^^

* ``/{dataViewName}/FastStatsSystems/{systemName}`` **GET**
    - Now returns ``PagedResults[FastStatsSystemDetail]`` (previously ``FastStatsSystemDetail``)
    - Spec incorrect - did not match API behaviour


Version 0.1.5
--------------

**03 Jul 2019**

* apteco-api commit: ``29ea3b2``
* (OrbitAPI version: ``1.8.3.915``)
* (OrbitAPI date: 21 Jun 2019)

*(Spec unchanged: keywords & classifiers added to* ``setup.py`` *)*


Version 0.1.4
--------------

**02 Jul 2019**

* apteco-api commit: ``7e7d09a``
* OrbitAPI version: ``1.8.3.915``
* OrbitAPI date: 21 Jun 2019

Added
^^^^^

* ``/About/Language`` **GET**
* ``/About/DataViews/{dataViewName}`` **GET**
* ``DataViewSummary``
* ``Capabilities``

Changed
^^^^^^^

* ``/About/DataViews`` **GET**, ``/About/DataViews/Domains/{domain}`` **GET**, ``/About/DataViews/Systems/{systemName}`` **GET**
    - returns ``PagedResults[DataViewSummary]`` (previously ``PagedResults[DataViewDetails]``)
* ``/{dataViewName}/FastStatsSystems/{systemName}/Folders`` **GET**
    - ``filter`` and ``orderBy`` parameters now also accept ``Type``, ``TableName``, ``VariableType`` fields, in addition to ``Name``, ``Description``
* ``/{dataViewName}/FastStatsSystems/{systemName}/Folders/{path}`` **GET**
    - now takes ``filter``, ``orderBy``, ``offset``, ``count`` parameters
* ``/{dataViewName}/FastStatsSystems/{systemName}/All`` **GET**
    - ``filter`` and ``orderBy`` parameters now also accept ``TableName``, ``VariableType`` fields, in addition to ``Key``, ``Type``
* ``/{dataViewName}/Sessions/LoginParameters`` **POST**, ``/{dataViewName}/Sessions/SaltedLogin`` **POST**, ``/{dataViewName}/Sessions/ConvertSession`` **POST**
    - now consumes ``application/x-www-form-urlencoded`` (previously ``multipart/form-data``)
* ``DataViewDetails``
    - ``capabilities`` now required
* ``FolderStructureNode``, ``FastStatsSystemItem``
    - ``variable`` property type now ``Variable`` (previously ``VariableItem``)

Removed
^^^^^^^

* ``/{dataViewName}/DataGrids/{systemName}/Files/{filePath}`` **POST**
* ``DataGridResult``
* ``VariableItem``


Version 0.1.0
--------------

**28 Jun 2019**

* apteco-api commit: ``e3fb422``
* OrbitAPI version: *(unknown)*
* OrbitAPI date: *(unknown)*

Initial version of the package.

Has the following endpoints (relevant to ``py-apteco``):

* *AboutApi* | **GET** ``/About/ExampleExperimentalResource`` | EXPERIMENTAL: Returns a sample string if experimental endpoints are enabled
* *AboutApi* | **GET** ``/About/ExampleUnderDevelopmentResource`` | UNDER DEVELOPMENT: Returns a sample string if under development endpoints are enabled
* *AboutApi* | **POST** ``/About/Process/ForceGarbageCollection`` | Requires OrbitAdmin: Forces a garbage collection in the API&#39;s process and then returns details about the API&#39;s .Net process
* *AboutApi* | **GET** ``/About/DataViews`` | Get the list of DataViews that are available.
* *AboutApi* | **GET** ``/About/DataViews/Domains/{domain}`` | Get the list of DataViews that are available to users with the specified email domain.
* *AboutApi* | **GET** ``/About/DataViews/Systems/{systemName}`` | Get the list of DataViews that are configured with the given FastStats system.
* *AboutApi* | **GET** ``/About/Endpoints`` | Returns details of all the endpoints in the API
* *AboutApi* | **GET** ``/About/Process`` | Requires OrbitAdmin: Returns details about the API&#39;s .Net process
* *AboutApi* | **GET** ``/About/Version`` | Returns version information about the API
* *CubesApi* | **POST** ``/{dataViewName}/Cubes/{systemName}/CalculateSync`` | EXPERIMENTAL: Calcaultes a cube using the given definition and returns the results.  The data to build the cube from is defined by the base query provided.
* *DataGridsApi* | **POST** ``/{dataViewName}/DataGrids/{systemName}/Files/{filePath}`` | EXPERIMENTAL: Returns the DataGrid from a saved file.
* *DirectoriesApi* | **DELETE** ``/{dataViewName}/Directories/{systemName}/{directoryPath}`` | Deletes directory at location
* *DirectoriesApi* | **GET** ``/{dataViewName}/Directories/{systemName}/{directoryPath}`` | Returns the list of files and subdirectories under the given directory
* *DirectoriesApi* | **GET** ``/{dataViewName}/Directories`` | Returns the list of systems that have access to a filesystem
* *DirectoriesApi* | **GET** ``/{dataViewName}/Directories/{systemName}`` | Returns the list of root directories configured in this FastStats system
* *DirectoriesApi* | **PUT** ``/{dataViewName}/Directories/{systemName}/{directoryPath}`` | Ensure that a directory exists in a location
* *ExportsApi* | **POST** ``/{dataViewName}/Exports/{systemName}/ExportSync`` | EXPERIMENTAL: Exports data using the given export definition and returns the results.  The results might contain the actual data in the \&quot;rows\&quot; part of the result or this might be written to a file.  The data to be exported is defined by the base query provided, along with any limits defined in the export request.
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}/All`` | Gets all FastStats systems items - variables, var codes, tables and folders
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}/Folders/{path}`` | Gets the folder structure for the FastStats system
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}/Folders`` | Gets the items in the root of the FastStats system folder structure
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}`` | Returns some top-level details for the specified FastStats system
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems`` | Returns the list of FastStats systems available
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}/Tables/{tableName}`` | Gets the details for a particular table in the FastStats system
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}/Tables`` | Gets all the tables present in the FastStats system
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}/Variables/{variableName}`` | Gets the details for a particular variable in the FastStats system
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}/Variables/{variableName}/Codes`` | Gets all the categories (var codes) for the specified variable in the FastStats system if it is a selector variable
* *FastStatsSystemsApi* | **GET** ``/{dataViewName}/FastStatsSystems/{systemName}/Variables`` | Gets all the variables present in the FastStats system
* *FastStatsSystemsApi* | **POST** ``/{dataViewName}/FastStatsSystems/{systemName}/RefreshInformationSync`` | Requires OrbitAdmin: An endpoint to request the API refresh any information it holds on the given FastStats system.  This endpoint will wait until the refresh has completed before returning.
* *FilesApi* | **DELETE** ``/{dataViewName}/Files/{systemName}/{filePath}`` | Deletes file at location
* *FilesApi* | **GET** ``/{dataViewName}/Files/{systemName}/{filePath}`` | Returns the contents for a file
* *FilesApi* | **PUT** ``/{dataViewName}/Files/{systemName}/{filePath}`` | Creates or updates a file at a location
* *QueriesApi* | **POST** ``/{dataViewName}/Queries/{systemName}/GetFileSync`` | EXPERIMENTAL: Get the query definition in the specified file
* *QueriesApi* | **POST** ``/{dataViewName}/Queries/{systemName}/CountSync`` | EXPERIMENTAL: Counts the given query and returns the results
* *QueriesApi* | **POST** ``/{dataViewName}/Queries/{systemName}/CountFileSync`` | EXPERIMENTAL: Counts the query in the specified file and returns the results
* *SessionsApi* | **POST** ``/{dataViewName}/Sessions/ConvertSession`` | Creates an API session token from a traditional FastStats session id
* *SessionsApi* | **POST** ``/{dataViewName}/Sessions/LoginParameters`` | Creates a new set of parameters to use when creating a new session via the salted login method.
* *SessionsApi* | **POST** ``/{dataViewName}/Sessions/SaltedLogin`` | Creates a session to use for other API requests
* *SessionsApi* | **POST** ``/{dataViewName}/Sessions/SimpleLogin`` | Creates a session to use for other API requests
* *SessionsApi* | **GET** ``/{dataViewName}/Sessions/{sessionId}`` | Gets some simple user details for the given session id
* *SessionsApi* | **GET** ``/{dataViewName}/Sessions`` | Requires OrbitAdmin: Gets some simple user details for all currently valid sessions.
* *SessionsApi* | **DELETE** ``/{dataViewName}/Sessions/{sessionId}`` | Logs out the specified session
