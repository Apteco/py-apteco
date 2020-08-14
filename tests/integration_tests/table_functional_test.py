class TestTableRelations:
    def test_eq(self, households, people, bookings, responses):
        assert households == households
        assert not households == people
        assert not households == bookings
        assert not households == responses

        assert not people == households
        assert people == people
        assert not people == bookings
        assert not people == responses

        assert not bookings == households
        assert not bookings == people
        assert bookings == bookings
        assert not bookings == responses

        assert not responses == households
        assert not responses == people
        assert not responses == bookings
        assert responses == responses

    def test_lt(self, households, people, bookings, responses):
        assert not households < households
        assert households < people
        assert households < bookings
        assert households < responses

        assert not people < households
        assert not people < people
        assert people < bookings
        assert people < responses

        assert not bookings < households
        assert not bookings < people
        assert not bookings < bookings
        assert not bookings < responses

        assert not responses < households
        assert not responses < people
        assert not responses < bookings
        assert not responses < responses

    def test_le(self, households, people, bookings, responses):
        assert households <= households
        assert households <= people
        assert households <= bookings
        assert households <= responses
        
        assert not people <= households
        assert people <= people
        assert people <= bookings
        assert people <= responses
        
        assert not bookings <= households
        assert not bookings <= people
        assert bookings <= bookings
        assert not bookings <= responses
        
        assert not responses <= households
        assert not responses <= people
        assert not responses <= bookings
        assert responses <= responses

    def test_gt(self, households, people, bookings, responses):
        assert not households > households
        assert not households > people
        assert not households > bookings
        assert not households > responses

        assert people > households
        assert not people > people
        assert not people > bookings
        assert not people > responses       

        assert bookings > households
        assert bookings > people
        assert not bookings > bookings
        assert not bookings > responses   

        assert responses > households
        assert responses > people
        assert not responses > bookings
        assert not responses > responses
        
    def test_ge(self, households, people, bookings, responses):
        assert households >= households
        assert not households >= people
        assert not households >= bookings
        assert not households >= responses

        assert people >= households
        assert people >= people
        assert not people >= bookings
        assert not people >= responses

        assert bookings >= households
        assert bookings >= people
        assert bookings >= bookings
        assert not bookings >= responses
        
        assert responses >= households
        assert responses >= people
        assert not responses >= bookings
        assert responses >= responses

    def test_ne(self, households, people, bookings, responses):
        assert people != bookings
        assert not people != people

    """def test_is_related(self, households, people, bookings, responses):
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
        assert responses.is_related(responses, allow_same=True)"""
