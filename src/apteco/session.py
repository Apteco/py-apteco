import getpass
import json
import warnings
from collections import Counter, defaultdict, namedtuple
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Tuple, Iterable

import apteco_api as aa
import PySimpleGUI

from apteco.data.apteco_logo import APTECO_LOGO
from apteco.exceptions import (
    ApiResultsError,
    DeserializeError,
    TablesError,
    VariablesError,
)
from apteco.query import TableMixin
from apteco.variables import (
    Variable,
    SelectorVariable,
    NumericVariable,
    TextVariable,
    ArrayVariable,
    FlagArrayVariable,
    DateVariable,
    DateTimeVariable,
    ReferenceVariable,
)

NOT_ASSIGNED: Any = object()
VARIABLES_PER_PAGE = 100


class Session:
    def __init__(self, credentials: "Credentials", system: str):
        self._unpack_credentials(credentials)
        self._create_client()
        self.system = system
        self._fetch_system_info()
        tables_without_vars, master_table_name = InitializeTablesAlgorithm(self).run()
        variables, self.tables = InitializeVariablesAlgorithm(
            self, tables_without_vars
        ).run()
        self.variables = VariablesAccessor(variables)
        self.master_table = self.tables[master_table_name]

    def _unpack_credentials(self, credentials):
        """Copy credentials data into session."""
        self.base_url = credentials.base_url
        self.data_view = credentials.data_view
        self.session_id = credentials.session_id
        self.access_token = credentials.access_token
        self.user = credentials.user

    def _create_client(self):
        """Create an authorized API client."""
        config = aa.Configuration()
        config.host = self.base_url
        config.api_key = {"Authorization": self.access_token}
        config.api_key_prefix = {"Authorization": "Bearer"}
        self._config = config
        self.api_client = aa.ApiClient(configuration=self._config)

    def _fetch_system_info(self):
        """Fetch FastStats system info from API and add to session."""
        systems_controller = aa.FastStatsSystemsApi(self.api_client)
        result = systems_controller.fast_stats_systems_get_fast_stats_system(
            self.data_view, self.system
        )
        self.system_info = FastStatsSystem(
            name=result.name,
            description=result.description,
            build_date=result.fast_stats_build_date,
            view_name=result.view_name,
        )

    def _to_dict(self):
        return {
            "base_url": self.base_url,
            "data_view": self.data_view,
            "session_id": self.session_id,
            "access_token": self.access_token,
            "user": self.user._asdict(),
            "system": self.system,
        }

    @staticmethod
    def _from_dict(d):
        try:
            credentials = Credentials(
                d["base_url"],
                d["data_view"],
                d["session_id"],
                d["access_token"],
                User(**d["user"]),
            )
            system = d["system"]
        except KeyError as e:
            raise DeserializeError(f"Data missing from 'Session' object: no {e} found.")
        except TypeError as exc:  # arguments missing from User __new__() call
            raise DeserializeError(
                f"The following parameter(s) were missing from 'User' object: "
                f"{exc.args[0].split(':')[1].strip()}"
            )
        else:
            return Session(credentials, system)

    def serialize(self):
        return json.dumps(self._to_dict())

    @staticmethod
    def deserialize(s: str):
        try:
            d = json.loads(s)
        except JSONDecodeError:
            raise DeserializeError("The given input could not be deserialized.")
        else:
            return Session._from_dict(d)


class Table(TableMixin):
    """Class representing a FastStats system table."""

    def __init__(
        self,
        name: str,
        singular_display_name: str,
        plural_display_name: str,
        is_default_table: bool,
        is_people_table: bool,
        total_records: int,
        child_relationship_name: str,
        parent_relationship_name: str,
        has_child_tables: bool,
        parent_name: str,
        parent: Optional["Table"],
        children: List["Table"],
        ancestors: List["Table"],
        descendants: List["Table"],
        variables: Dict[str, Variable],
        *,
        session: Optional[Session] = None,
    ):
        """

        Args:
            name (str): table reference name
            singular_display_name (str): noun for a single item
                from this table
            plural_display_name (str): noun for multiple items
                from this table
            is_default_table (bool): flag if this is the default table
                for this FastStats system
            is_people_table (bool): flag if this is the table
                representing people in this FastStats system
            total_records (int): total number of records on this table
            child_relationship_name (str): phrase to relate
                to this table from its parent,
                e.g. 'customer <purchased the> product'
            parent_relationship_name (str): phrase to relate this table
                to its parent,
                e.g. 'product <was purchased by the> customer'
            has_child_tables (bool): flag if this table
                has any child tables
            parent_name (str): name of this table's parent table
                (an empty string for the master table)
            parent (Table): the parent table of this table
                (``None`` for the master table)
            children (List[Table]): list of child tables of this table
                (an empty list if table has no children)
            ancestors (List[Table]): list of ancestor tables
                of this table (an empty list for the master table)
            descendants (List[Table]): list of descendant tables
                of this table (an empty list if table has no children)
            variables (Dict[str, Variable]): variables on this table,
                mapping from variable description
                to its Variable object
            session (Session): API session the tables data belongs to

        """
        self.name = name
        self.singular_display_name = singular_display_name
        self.plural_display_name = plural_display_name
        self.is_default_table = is_default_table
        self.is_people_table = is_people_table
        self.total_records = total_records
        self.child_relationship_name = child_relationship_name
        self.parent_relationship_name = parent_relationship_name
        self.has_child_tables = has_child_tables
        self.parent_name = parent_name
        self.parent = parent
        self.children = children
        self.ancestors = ancestors
        self.descendants = descendants
        self.variables = variables
        self.session = session

    def is_same(self, other: "Table"):
        """Return whether this table is the same as ``other``.

        Args:
            other (Table): the table to check against

        Returns:
            bool: ``True`` if this is the same as ``other``, otherwise ``False``

        """
        return self.name == other.name

    def is_ancestor(self, other: "Table", allow_same: bool = False):
        """Return whether this table is an ancestor of ``other``.

        Args:
            other (Table): the table to check against
            allow_same (bool): whether to include the table itself as an 'ancestor'
                (default is ``False``)

        Returns:
            bool: ``True`` if this is an ancestor of ``other``, otherwise ``False``

        """
        return self in other.ancestors or (allow_same and self.is_same(other))

    def is_descendant(self, other: "Table", allow_same: bool = False):
        """Return whether this table is a descendant of ``other``.

        Args:
            other (Table): the table to check against
            allow_same (bool): whether to include the table itself as an 'ancestor'
                (default is ``False``)

        Returns:
            bool: ``True`` if this is a descendant of ``other``, otherwise ``False``

        """
        return self in other.descendants or (allow_same and self.is_same(other))

    def is_related(self, other: "Table", allow_same: bool = False):
        """Return whether this table is related to ``other``.

        'related' is defined as being either an ancestor or descendant.

        Args:
            other (Table): the table to check against
            allow_same (bool): whether to include the table itself as 'related'
                (default is ``False``)

        Returns:
            bool: ``True`` if this is related to ``other``, otherwise ``False``

        """
        return (
            self.is_ancestor(other)
            or self.is_descendant(other)
            or (allow_same and self.is_same(other))
        )

    def __eq__(self, other):
        """Return whether this is the same table as ``other``."""
        return self.is_same(other)

    def __lt__(self, other):
        """Return whether this table is an ancestor of ``other``."""
        return self.is_ancestor(other)

    def __gt__(self, other):
        """Return whether this table is a descendant of ``other``."""
        return self.is_descendant(other)

    def __le__(self, other):
        """Return whether this table is the same or an ancestor of ``other``."""
        return self.is_ancestor(other, allow_same=True)

    def __ge__(self, other):
        """Return whether this table is the same or a descendant of ``other``."""
        return self.is_descendant(other, allow_same=True)

    def __getitem__(self, item):
        return self.variables[item]


User = namedtuple("User", ["username", "first_name", "surname", "email_address"])


class Credentials:
    """Class to hold credentials from the simple login process."""

    def __init__(
        self,
        base_url: str,
        data_view: str,
        session_id: str,
        access_token: str,
        user: User,
    ):
        """

        Args:
            base_url (str): API base URL, normally ending '/OrbitAPI'
            data_view (str): name of data view
            session_id (str): Apteco session ID
            access_token (str): access token for current session
            user (User): API user

        """
        self.base_url = base_url
        self.data_view = data_view
        self.session_id = session_id
        self.access_token = access_token
        self.user = user


FastStatsSystem = namedtuple(
    "FastStatsSystem", ["name", "description", "build_date", "view_name"]
)


def login(base_url: str, data_view: str, system: str, user: str) -> Session:
    """Log in to the API without supplying password directly.

    Args:
        base_url (str): API base URL, normally ending '/OrbitAPI'
        data_view (str): DataView being logged into
        system (str): FastStats system to connect to
        user (str): username of API user

    Returns:
        Session: API session object

    """
    return login_with_password(
        base_url, data_view, system, user, password=_get_password()
    )


def login_with_password(
    base_url: str, data_view: str, system: str, user: str, password: str
) -> Session:
    """Log in to the API, supplying password directly.

    Args:
        base_url (str): API base URL, normally ending '/OrbitAPI'
        data_view (str): DataView being logged into
        system (str): FastStats system to connect to
        user (str): username of API user
        password (str): password for this user

    Returns:
        Session: API session object

    """
    credentials = SimpleLoginAlgorithm(base_url, data_view).run(user, password)
    return Session(credentials, system)


def _get_password(prompt: str = "Enter your password: ") -> str:
    """Get password from user without displaying it on screen."""
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("error")
            return getpass.getpass(prompt)
    except getpass.GetPassWarning:
        return PySimpleGUI.PopupGetText(
            prompt,
            password_char="*",
            title="Apteco API",
            button_color=("#ffffff", "#004964"),
            icon=APTECO_LOGO,
        )


# https://gieseanw.wordpress.com/2019/05/10/algorithms-as-objects/
class SimpleLoginAlgorithm:
    """Class holding the algorithm to carry out a simple login.

    Attributes:
        base_url (str): API base URL, normally ending '/OrbitAPI'
        data_view (str): DataView being logged into
        api_client (aa.ApiClient): API client used to log in
        session_id (str): Apteco session ID for the created session
        access_token (str): access token for the created session
        user (User): API user

    Methods:
        run(): entry point to run the algorithm

    """

    def __init__(self, base_url: str, data_view: str):
        """

        Args:
            base_url (str): API base URL, normally ending '/OrbitAPI'
            data_view (str): DataView being logged into

        """
        self.base_url = base_url
        self.data_view = data_view

    def run(self, user: str, password: str) -> Credentials:
        """Run the algorithm with the given login credentials.

        Args:
            user (str): username of API user
            password (str): password for this user

        Returns:
            Credentials: API session credentials

        """
        self._create_unauthorized_client()
        self._simple_login(user, password)
        self._create_credentials()
        return self.credentials

    def _create_unauthorized_client(self):
        """Create an unauthorized API client."""
        config = aa.Configuration()
        config.host = self.base_url
        self._config = config
        self.api_client = aa.ApiClient(configuration=self._config)

    def _simple_login(self, user, password):
        """Call API to perform simple login."""
        sessions_controller = aa.SessionsApi(self.api_client)
        login_response = sessions_controller.sessions_create_session_simple(
            self.data_view, user, password
        )
        self.session_id = login_response.session_id
        self.access_token = login_response.access_token
        self.user = User(
            username=login_response.user.username,
            first_name=login_response.user.firstname,
            surname=login_response.user.surname,
            email_address=login_response.user.email_address,
        )

    def _create_credentials(self):
        """Initialize session credentials object."""
        self.credentials = Credentials(
            self.base_url, self.data_view, self.session_id, self.access_token, self.user
        )


class InitializeTablesAlgorithm:
    """Class holding the algorithm to initialize system tables.

    The purpose of this algorithm is to
    retrieve the raw tables data for the given system,
    process it to infer parent and child table relationships,
    convert the raw tables into py-apteco Table objects,
    and assign to these tables their relationships to other tables.

    Attributes:
        data_view (str): DataView the system belongs to
        system (str): FastStats system the session is connected to
        api_client (aa.ApiClient): client to handle API calls
        session (Session): API session the tables data belongs to
        raw_tables (List[aa.Table]): list of raw tables
        children_lookup (Dict[str, List[str]]): mapping from table name
            to list of its child table names
        master_table (Table): master table of the FastStats system
        tables (Dict[str, Table]): mapping from table name
            to its Table object

    Methods:
        run(): entry point to run the algorithm

    """

    def __init__(self, session):
        """

        Args:
            session (Session): API session the tables data belongs to

        """
        self.data_view = session.data_view
        self.system = session.system
        self.api_client = session.api_client
        self.session = session

    def run(self) -> Tuple[Dict[str, Table], str]:
        """Run the algorithm.

        Returns:
            (tuple): tuple containing:

                tables (Dict[str, Table]): mapping from table name
                    to its Table object
                master_table_name (str):
                    name of the master table of the FastStats system

        """
        self._get_raw_tables()
        self._identify_children()
        self._create_tables()
        self._assign_parent_and_children()
        self._find_master_table()
        _tree_tables = self._assign_ancestors_and_descendants(self.master_table, [])
        self._check_all_tables_in_tree(_tree_tables)
        self._check_all_relations_assigned()
        return self.tables, self.master_table.name

    def _get_raw_tables(self):
        """Get list of all tables from API."""
        systems_controller = aa.FastStatsSystemsApi(self.api_client)
        results = systems_controller.fast_stats_systems_get_fast_stats_tables(
            self.data_view, self.system, count=1000
        )
        self._check_table_results_consistency(results)
        self.raw_tables = results.list

    @staticmethod
    def _check_table_results_consistency(results: aa.PagedResultsTable):
        """Check the number of tables in list matches stated count."""
        results_count = results.count
        list_count = len(results.list)
        if not results_count == list_count:
            raise ApiResultsError(
                f"API stated {results_count} tables were returned"
                f" but {list_count} were found."
            )

    def _identify_children(self):
        """Identify child tables for each table."""
        self.children_lookup = defaultdict(list)
        for table in self.raw_tables:
            self.children_lookup[table.parent_table].append(table.name)
        # don't freeze yet: will need to look up childless tables and return empty list

    def _create_tables(self):
        """Create py-apteco tables from apteco_api ones."""
        self.tables = {
            t.name: Table(
                t.name,
                t.singular_display_name,
                t.plural_display_name,
                t.is_default_table,
                t.is_people_table,
                t.total_records,
                t.child_relationship_name,
                t.parent_relationship_name,
                t.has_child_tables,
                t.parent_table,
                NOT_ASSIGNED,
                NOT_ASSIGNED,
                NOT_ASSIGNED,
                NOT_ASSIGNED,
                NOT_ASSIGNED,
                session=self.session,
            )
            for t in self.raw_tables
        }

    def _assign_parent_and_children(self):
        """Assign parent and children attributes for each table."""
        for table in self.tables.values():
            if table.parent_name == "":
                table.parent = None
            else:
                table.parent = self.tables[table.parent_name]
            table.children = [
                self.tables[name] for name in self.children_lookup[table.name]
            ]
            self._check_child_tables_consistency(table)
        self.children_lookup.default_factory = None  # 'freeze' as normal dict

    @staticmethod
    def _check_child_tables_consistency(table: Table):
        """Check table's children matches ```has_child_tables```."""
        if table.has_child_tables and not table.children:
            raise TablesError(
                f"API stated '{table.name}' table has child tables but none were found."
            )
        if not table.has_child_tables and table.children:
            raise TablesError(
                f"API stated '{table.name}' table has no child tables"
                f" but {len(table.children)} were found."
            )

    def _find_master_table(self):
        """Retrieve master table, ensuring there is exactly one."""
        try:
            (master_table_name,) = self.children_lookup[""]
        except KeyError:
            raise TablesError("No master table found.")
        except ValueError:  # unpacking failed => !=1 master tables
            raise TablesError(
                f"Found {len(self.children_lookup[''])} master tables,"
                f" there should be 1."
            )
        try:
            self.master_table = self.tables[master_table_name]
        except KeyError:
            raise TablesError(
                f"The master table '{master_table_name}' could not be found."
            )

    def _assign_ancestors_and_descendants(
        self, table: Table, ancestors: List[Table]
    ) -> List[Table]:
        """Assign ancestor and descendant tables for each table."""
        table.ancestors = ancestors
        table.descendants = [
            descendant
            for child in table.children
            for descendant in self._assign_ancestors_and_descendants(
                child, [table] + table.ancestors
            )
        ]
        return [table] + table.descendants

    def _check_all_tables_in_tree(self, _tree_tables):
        """Check all tables appear in table tree exactly once."""
        tree_tables_counter = Counter(t.name for t in _tree_tables)
        raw_tables_counter = Counter(t.name for t in self.raw_tables)
        if not tree_tables_counter == raw_tables_counter:
            diff = Counter(tree_tables_counter)
            diff.subtract(raw_tables_counter)
            raise TablesError(
                f"Error constructing table tree:"
                f" {len(+diff)} table(s) occurred more than once in tree"
                f" and {len(-diff)} table(s) did not occur at all."
            )

    def _check_all_relations_assigned(self):
        """Check tables have all relation attributes assigned."""
        relations = ["parent", "children", "ancestors", "descendants"]
        no_relation = defaultdict(list)
        for table in self.tables.values():
            for rel in relations:
                if getattr(table, rel) is NOT_ASSIGNED:
                    no_relation[rel].append(table.name)
        error_details = ""
        for rel in relations:
            if no_relation[rel]:
                error_details += (
                    f"\n{len(no_relation[rel])} table(s) had no {rel} assigned."
                    f" First example: '{no_relation[rel][0]}' table"
                )
        if error_details:
            raise TablesError("Error constructing table tree:" + error_details)


class InitializeVariablesAlgorithm:
    """Class holding the algorithm to initialize system variables.

    The purpose of this algorithm is to
    retrieve the raw variables for the given system,
    convert them into py-apteco Variable objects,
    and assign these to their tables.

    Attributes:
        data_view (str): DataView the system belongs to
        system (str): FastStats system the session is connected to
        api_client (aa.ApiClient): client to handle API calls
        session (Session): API session the variables data belongs to
        tables (Dict[str, Table]): mapping from table name
            to its Table object
        raw_variables (List[aa.Variable]): list of raw variables
        variables (List[Variable]): list of variables as py-apteco Variable objects
        variables_lookup (Dict[str, List[str]]): mapping from table name
            to list of its variables

    Methods:
        run(): entry point to run the algorithm

    """

    def __init__(self, session, tables_without_variables):
        """

        Args:
            session (Session): API session the variables data belongs to
            tables_without_variables (Dict[str, Table]): mapping from
                table name to its Table object
                with variables attribute as ``NOT_ASSIGNED``

        """
        self.data_view = session.data_view
        self.system = session.system
        self.api_client = session.api_client
        self.session = session
        self.tables = tables_without_variables

    def run(self) -> Tuple[List[Variable], Dict[str, Table]]:
        """Run the algorithm.

        Returns:
            (tuple): tuple containing:

                variables (List[Variable]): list of variables
                    as py-apteco Variable objects
                tables (Dict[str, Table]): mapping from table name
                    to its Table object, initially with
                    ``variables`` attribute as ``NOT_ASSIGNED``

        """

        self._get_raw_variables()
        self._create_variables()
        self._identify_variables()
        self._assign_variables()
        self._check_all_variables_assigned()
        return self.variables, self.tables

    def _get_raw_variables(self, variables_per_page=VARIABLES_PER_PAGE):
        """Get list of all variables from API."""
        systems_controller = aa.FastStatsSystemsApi(self.api_client)

        self.raw_variables = []
        offset = 0
        while True:
            results = systems_controller.fast_stats_systems_get_fast_stats_variables(
                self.data_view, self.system, count=variables_per_page, offset=offset
            )  # type: aa.PagedResultsVariable
            self.raw_variables.extend(results.list)
            if results.offset + results.count >= results.total_count:
                break
            offset = results.offset + results.count
        self._check_variable_results_consistency(results.total_count)

    def _check_variable_results_consistency(self, total_variables: int):
        """Check number of variables returned matches stated total count."""
        list_count = len(self.raw_variables)
        if not total_variables == list_count:
            raise ApiResultsError(
                f"API stated there are {total_variables} variables in the system"
                f" but {list_count} were returned."
            )

    def _create_variables(self):
        """Create py-apteco variables from apteco_api ones."""
        self.variables = [
            self._choose_variable(v)(
                name=v.name,
                description=v.description,
                type=v.type,
                folder_name=v.folder_name,
                table=self.tables[v.table_name],
                is_selectable=v.is_selectable,
                is_browsable=v.is_browsable,
                is_exportable=v.is_exportable,
                is_virtual=v.is_virtual,
                selector_info=v.selector_info,
                numeric_info=v.numeric_info,
                text_info=v.text_info,
                reference_info=v.reference_info,
                session=self.session,
            )
            for v in self.raw_variables
        ]

    @staticmethod
    def _choose_variable(raw_variable: aa.Variable):
        """Get class to create given variable according to its type."""
        variable_type_lookup = {
            ("Selector", "Categorical", "SingleValue", False): SelectorVariable,
            ("Selector", "Categorical", "SingleValue", True,): SelectorVariable,  # should be Combined Categories type
            ("Numeric", None, None, False): NumericVariable,
            ("Text", None, None, False): TextVariable,
            ("Selector", "Categorical", "OrArray", False): ArrayVariable,
            ("Selector", "Categorical", "OrArray", True): ArrayVariable,  # should be Combined Categories type
            ("Selector", "Categorical", "OrBitArray", False): FlagArrayVariable,
            ("Selector", "Categorical", "OrBitArray", True): FlagArrayVariable,  # should be Combined Categories type
            ("Selector", "Date", "SingleValue", False): DateVariable,
            ("Selector", "Date", "OrBitArray", False): FlagArrayVariable,  # some kind of VV
            ("Selector", "DateTime", "SingleValue", False): DateTimeVariable,
            ("Reference", None, None, False): ReferenceVariable,
        }

        determinant = (
            raw_variable.type,
            (raw_variable.to_dict().get("selector_info") or {}).get("sub_type"),
            (raw_variable.to_dict().get("selector_info") or {}).get("selector_type"),
            bool(
                (raw_variable.to_dict().get("selector_info") or {}).get(
                    "combined_from_variable_name"
                )
            ),
        )
        try:
            return variable_type_lookup[determinant]
        except KeyError as exc:
            raise VariablesError(
                f"Failed to initialize variable '{raw_variable.name}',"
                f" did not recognise the type from determinant: {determinant}"
            ) from exc

    def _identify_variables(self):
        """Identify variables for each table."""
        self.variables_lookup = defaultdict(list)
        for variable in self.variables:
            self.variables_lookup[variable.table_name].append(variable)
        self.variables_lookup.default_factory = None  # 'freeze' as normal dict

    def _assign_variables(self):
        """Assign variables to each table."""
        for table in self.tables.values():
            try:
                table.variables = VariablesAccessor(self.variables_lookup[table.name])
            except KeyError:
                raise VariablesError(f"No variables found for '{table.name}' table.")

    def _check_all_variables_assigned(self):
        """Check all tables have variables attribute assigned."""
        no_variables = []
        for table in self.tables.values():
            if table.variables is NOT_ASSIGNED:
                no_variables.append(table.name)
        if no_variables:
            raise VariablesError(
                f"{len(no_variables)} table(s) had no variables assigned."
            )


class VariablesAccessor:
    """Dictionary-like access for variables by name or description."""

    def __init__(self, variables: Iterable[Variable]):
        self._variables_by_name = {var.name: var for var in variables}
        self._variables_by_desc = {var.description: var for var in variables}
        self._variables = variables

    def __getitem__(self, item):
        name_match = self._variables_by_name.get(item)
        desc_match = self._variables_by_desc.get(item)
        match_count = (name_match is not None) + (desc_match is not None)
        if match_count == 1:
            return name_match or desc_match
        elif match_count == 2:
            if name_match == desc_match:
                return name_match
            raise KeyError(f"Lookup key '{item}' was ambiguous.")
        else:
            raise KeyError(
                f"Lookup key '{item}' did not match a variable name or description."
            )

    def __iter__(self):
        return iter(self._variables)
