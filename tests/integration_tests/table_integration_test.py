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
