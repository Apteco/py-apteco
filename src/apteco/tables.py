from typing import Iterable, List, Optional

from apteco.query import TableMixin


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
        variables: "VariablesAccessor",
        *,
        session: Optional["Session"] = None,
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
            variables (VariablesAccessor): variables on this table
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


class TablesAccessor:
    """List- and dictionary-like access for tables."""

    def __init__(self, tables: Iterable[Table]):
        self._tables = list(tables)
        self._tables_by_name = {table.name: table for table in self._tables}

    def __len__(self):
        return len(self._tables)

    def __iter__(self):
        return iter(self._tables)

    def __getitem__(self, item):
        try:
            return self._tables_by_name[item]
        except KeyError as exc:
            raise KeyError(f"Lookup key '{item}' did not match a table name.") from exc
