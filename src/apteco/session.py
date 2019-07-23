import getpass
import warnings
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import apteco_api as aa
import PySimpleGUI

from apteco.exceptions import ApiResultsError, AptecoTablesError

ICON = Path(__file__).absolute().parent / "data/apteco_logo.ico"
NOT_ASSIGNED: Any = object()


class Session:
    def __init__(self, credentials: "Credentials", system: str):
        self._unpack_credentials(credentials)
        self.system = system
        self.tables, self.master_table = InitialiseTablesAlgorithm(self).run()

    def _unpack_credentials(self, credentials):
        self.base_url = credentials.base_url
        self.data_view = credentials.data_view
        self.api_client = credentials.api_client
        self._config = self.api_client.configuration
        self.session_id = credentials.session_id
        self.access_token = credentials.access_token
        self.user = credentials.user


class Table:
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
                (```None``` for the master table)
            children (List[Table]): list of child tables of this table
                (an empty list if table has no children)
            ancestors (List[Table]): list of ancestor tables
                of this table (an empty list for the master table)
            descendants (List[Table]): list of descendant tables
                of this table (an empty list if table has no children)
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
        self.session = session


# TODO: make dataclass when Python 3.7
class User:
    """Class representing an API user."""

    def __init__(
        self, username: str, first_name: str, surname: str, email_address: str
    ):
        """

        Args:
            username (str): username (used to log in)
            first_name (str): user's first name
            surname (str): user's surname
            email_address (str): user's email address

        """
        self.username = username
        self.first_name = first_name
        self.surname = surname
        self.email_address = email_address


# TODO: make dataclass when Python 3.7
class Credentials:
    """Class to hold credentials from the simple login process."""

    def __init__(
        self,
        base_url: str,
        data_view: str,
        api_client: aa.ApiClient,
        session_id: str,
        access_token: str,
        user: User,
    ):
        """

        Args:
            base_url (str): API base URL, normally ending '/OrbitAPI'
            data_view (str): name of data view
            api_client (aa.ApiClient): client for handling API calls
            session_id (str): Apteco session ID
            access_token (str): access token for current session
            user (User): API user

        """
        self.base_url = base_url
        self.data_view = data_view
        self.api_client = api_client
        self.session_id = session_id
        self.access_token = access_token
        self.user = user


def login(base_url: str, data_view: str, user: str) -> Credentials:
    """Log in to the API without supplying password directly.

    Args:
        base_url (str): API base URL, normally ending '/OrbitAPI'
        data_view (str): DataView being logged into
        user (str): username of API user

    Returns:
        Credentials: API session credentials

    """
    return login_with_password(base_url, data_view, user, password=_get_password())


def login_with_password(
    base_url: str, data_view: str, user: str, password: str
) -> Credentials:
    """Log in to the API, supplying password directly.

    Args:
        base_url (str): API base URL, normally ending '/OrbitAPI'
        data_view (str): DataView being logged into
        user (str): username of API user
        password (str): password for this user

    Returns:
        Credentials: API session credentials

    """
    return SimpleLoginAlgorithm(base_url, data_view).run(user, password)


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
            icon=ICON,
        )


# https://gieseanw.wordpress.com/2019/05/10/algorithms-as-objects/
class SimpleLoginAlgorithm:
    """Class holding the algorithm to carry out a simple login.

    Attributes:
        base_url (str): API base URL, normally ending '/OrbitAPI'
        data_view (str): DataView being logged into
        api_client (aa.ApiClient): API client being created
            and authorised during login
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
        self._create_client()
        self._simple_login(user, password)
        self._set_authorization(self.access_token)
        self._create_credentials()
        return self.credentials

    def _create_client(self):
        """Create an API client."""
        self._config = aa.Configuration(host=self.base_url)
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
            login_response.user.username,
            login_response.user.firstname,
            login_response.user.surname,
            login_response.user.email_address,
        )

    def _set_authorization(self, access_token):
        """Set authorization properties on API client configuration."""
        self._config.api_key = {"Authorization": access_token}
        self._config.api_key_prefix = {"Authorization": "Bearer"}

    def _create_credentials(self):
        """Initialise session credentials object."""
        self.credentials = Credentials(
            self.base_url,
            self.data_view,
            self.api_client,
            self.session_id,
            self.access_token,
            self.user,
        )


class InitialiseTablesAlgorithm:
    """Class holding the algorithm to initialise system tables.

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
        raw_tables (Dict[str, aa.Table]): mapping from table name
            to its raw table data
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

    def run(self) -> Tuple[Dict[str, Table], Table]:
        """Run the algorithm.

        Returns:
            (tuple): tuple containing:

                tables (Dict[str, Table]): mapping from table name
                    to its Table object
                master_table (Table):
                    master table of the FastStats system

        """
        self._get_raw_tables()
        self._identify_children()
        self._create_tables()
        self._assign_parent_and_children()
        self._find_master_table()
        _tree_tables = self._assign_ancestors_and_descendants(self.master_table, [])
        self._check_all_tables_in_tree(_tree_tables)
        self._check_all_relations_assigned()
        return self.tables, self.master_table

    def _get_raw_tables(self):
        """Get list of all tables from API."""
        systems_controller = aa.FastStatsSystemsApi(self.api_client)
        results = systems_controller.fast_stats_systems_get_fast_stats_tables(
            self.data_view, self.system
        )
        self._check_table_results_consistency(results)
        self.raw_tables = {t.name: t for t in results.list}

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
        for table in self.raw_tables.values():
            self.children_lookup[table.parent_table].append(table.name)

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
                session=self.session,
            )
            for t in self.raw_tables.values()
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
            raise AptecoTablesError(
                f"API stated {table.name} has child tables but none were found."
            )
        if not table.has_child_tables and table.children:
            raise AptecoTablesError(
                f"API stated {table.name} has no child tables"
                f" but {len(table.children)} were found."
            )

    def _find_master_table(self):
        """Retrieve master table, ensuring there is exactly one."""
        try:
            (master_table_name,) = self.children_lookup[""]
            self.master_table = self.tables[master_table_name]
        except KeyError:
            raise AptecoTablesError("No master table found.")
        except ValueError:  # unpacking failed => !=1 master tables
            raise AptecoTablesError(
                f"Found {len(self.children_lookup[''])} master tables,"
                f" there should only be 1."
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
        raw_tables_counter = Counter(name for name in self.raw_tables.keys())
        if not tree_tables_counter == raw_tables_counter:
            diff = Counter({k: v for k, v in tree_tables_counter.items()})
            diff.subtract(raw_tables_counter)
            raise AptecoTablesError(
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
        for rel in relations:
            if no_relation[rel]:
                raise AptecoTablesError(
                    f"Error constructing table tree:"
                    f" {len(no_relation[rel])} table(s) had no {rel} assigned."
                    f" First example: table '{no_relation[rel][0]}'"
                )
