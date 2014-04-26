def test_create_user():
    """
    When I instantiate a user with a valid username, email, and password
    Then I should get a valid user object
    And the user should be stored in the database
    And the password should be encrypted in the database
    """
    pass


def test_create_user_no_username():
    """
    When I create a new user
    And the username isn't set
    Then it should assert an error
    """
    pass


def test_create_user_exists():
    """
    When I create a new user
    And the username already exists in the system
    Then it should assert an error
    """
    pass


def test_create_user_no_email():
    """
    When I create a new user
    And the email address isn't set
    Then it should assert an error
    """
    pass


def test_create_user_not_email():
    """
    When I create a new user
    And the email address isn't an email address
    Then it should assert an error
    """
    pass


def test_create_user_email_exists():
    """
    When I create a new user
    And the email already exists in the system
    Then it should assert an error
    """
    pass


def test_create_user_no_password():
    """
    When I create a new user
    And the password isn't set
    Then it should assert an error
    """
    pass


def test_create_user_short_password():
    """
    When I create a new user
    And the password is less than 8 characters long
    Then it should assert an error
    """
    pass


def test_create_user_password_contains_username():
    """
    When I create a new user
    And the password contains the username or email
    Then it should assert an error
    """
    pass


def test_api_create_user():
    """
    When I create a new user by hitting the API
    Then I should get a user JSON
    """
    pass


def test_api_create_user_error():
    """
    When I try to create a new user by hitting the API
    And I provide problematic information
    Then I should get an error JSON
    """
    pass
