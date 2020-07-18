class TestTableRelations:
    def test_is_same(self, households, people, bookings, responses):
        assert households.is_same(households)
        assert not households.is_same(people)
        assert not households.is_same(bookings)
        assert not households.is_same(responses)

        assert not people.is_same(households)
        assert people.is_same(people)
        assert not people.is_same(bookings)
        assert not people.is_same(responses)

        assert not bookings.is_same(households)
        assert not bookings.is_same(people)
        assert bookings.is_same(bookings)
        assert not bookings.is_same(responses)

        assert not responses.is_same(households)
        assert not responses.is_same(people)
        assert not responses.is_same(bookings)
        assert responses.is_same(responses)

    def test_is_ancestor(self, households, people, bookings, responses):
        assert not households.is_ancestor(households)
        assert households.is_ancestor(people)
        assert households.is_ancestor(bookings)
        assert households.is_ancestor(responses)
        assert households.is_ancestor(households, allow_same=True)
        assert households.is_ancestor(people, allow_same=True)
        assert households.is_ancestor(bookings, allow_same=True)
        assert households.is_ancestor(responses, allow_same=True)

        assert not people.is_ancestor(households)
        assert not people.is_ancestor(people)
        assert people.is_ancestor(bookings)
        assert people.is_ancestor(responses)
        assert not people.is_ancestor(households, allow_same=True)
        assert people.is_ancestor(people, allow_same=True)
        assert people.is_ancestor(bookings, allow_same=True)
        assert people.is_ancestor(responses, allow_same=True)

        assert not bookings.is_ancestor(households)
        assert not bookings.is_ancestor(people)
        assert not bookings.is_ancestor(bookings)
        assert not bookings.is_ancestor(responses)
        assert not bookings.is_ancestor(households, allow_same=True)
        assert not bookings.is_ancestor(people, allow_same=True)
        assert bookings.is_ancestor(bookings, allow_same=True)
        assert not bookings.is_ancestor(responses, allow_same=True)

        assert not responses.is_ancestor(households)
        assert not responses.is_ancestor(people)
        assert not responses.is_ancestor(bookings)
        assert not responses.is_ancestor(responses)
        assert not responses.is_ancestor(households, allow_same=True)
        assert not responses.is_ancestor(people, allow_same=True)
        assert not responses.is_ancestor(bookings, allow_same=True)
        assert responses.is_ancestor(responses, allow_same=True)

    def test_is_descendant(self, households, people, bookings, responses):
        assert not households.is_descendant(households)
        assert not households.is_descendant(people)
        assert not households.is_descendant(bookings)
        assert not households.is_descendant(responses)
        assert households.is_descendant(households, allow_same=True)
        assert not households.is_descendant(people, allow_same=True)
        assert not households.is_descendant(bookings, allow_same=True)
        assert not households.is_descendant(responses, allow_same=True)

        assert people.is_descendant(households)
        assert not people.is_descendant(people)
        assert not people.is_descendant(bookings)
        assert not people.is_descendant(responses)
        assert people.is_descendant(households, allow_same=True)
        assert people.is_descendant(people, allow_same=True)
        assert not people.is_descendant(bookings, allow_same=True)
        assert not people.is_descendant(responses, allow_same=True)

        assert bookings.is_descendant(households)
        assert bookings.is_descendant(people)
        assert not bookings.is_descendant(bookings)
        assert not bookings.is_descendant(responses)
        assert bookings.is_descendant(households, allow_same=True)
        assert bookings.is_descendant(people, allow_same=True)
        assert bookings.is_descendant(bookings, allow_same=True)
        assert not bookings.is_descendant(responses, allow_same=True)

        assert responses.is_descendant(households)
        assert responses.is_descendant(people)
        assert not responses.is_descendant(bookings)
        assert not responses.is_descendant(responses)
        assert responses.is_descendant(households, allow_same=True)
        assert responses.is_descendant(people, allow_same=True)
        assert not responses.is_descendant(bookings, allow_same=True)
        assert responses.is_descendant(responses, allow_same=True)

    def test_is_related(self, households, people, bookings, responses):
        assert not households.is_related(households)
        assert households.is_related(people)
        assert households.is_related(bookings)
        assert households.is_related(responses)
        assert households.is_related(households, allow_same=True)
        assert households.is_related(people, allow_same=True)
        assert households.is_related(bookings, allow_same=True)
        assert households.is_related(responses, allow_same=True)

        assert people.is_related(households)
        assert not people.is_related(people)
        assert people.is_related(bookings)
        assert people.is_related(responses)
        assert people.is_related(households, allow_same=True)
        assert people.is_related(people, allow_same=True)
        assert people.is_related(bookings, allow_same=True)
        assert people.is_related(responses, allow_same=True)

        assert bookings.is_related(households)
        assert bookings.is_related(people)
        assert not bookings.is_related(bookings)
        assert not bookings.is_related(responses)
        assert bookings.is_related(households, allow_same=True)
        assert bookings.is_related(people, allow_same=True)
        assert bookings.is_related(bookings, allow_same=True)
        assert not bookings.is_related(responses, allow_same=True)

        assert responses.is_related(households)
        assert responses.is_related(people)
        assert not responses.is_related(bookings)
        assert not responses.is_related(responses)
        assert responses.is_related(households, allow_same=True)
        assert responses.is_related(people, allow_same=True)
        assert not responses.is_related(bookings, allow_same=True)
        assert responses.is_related(responses, allow_same=True)


def test_variables_getitem_by_name(bookings):
    destination = bookings.variables["boDest"]
    assert destination.description == "Destination"


def test_variables_getitem_by_desc(bookings):
    destination = bookings.variables["Destination"]
    assert destination.name == "boDest"


def test_variables_iter(bookings):
    all_vars = []
    for var in bookings.variables:
        if not var.is_virtual:
            all_vars.append(var.name)

    assert sorted(all_vars) == [
        "boCont",
        "boCost",
        "boDate",
        "boDest",
        "boKeyCd",
        "boProd",
        "boProfit",
        "boTrav",
        "boURN",
        "deFacil",
        "deGrade",
        "deMgr",
        "deType",
    ]
