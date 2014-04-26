def test_get_user_other():
    """
    When I get a user
    And I'm not that user
    Then I should not get their email or password
    """
    pass


def test_get_user_self():
    """
    When I get a user
    And I am that user
    Then I should get the email, but not the password
    """
    pass


def test_get_user_none():
    """
    When I get a user by ID
    And no user exists by that ID
    Then I should get a 404 response
    """
    pass


def test_get_user():
    """
    When I get a user by ID
    And a user exists for that ID
    Then I should get a user
    """
    pass
