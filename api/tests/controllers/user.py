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


def test_update_user_password():
    """
    When I update a user's password
    Then the password should be encrypted in the database
    """
    pass


def test_login_user_no_username():
    """
    When I try to login
    And I don't provide a username
    Then it should 404, not match
    """
    pass


def test_login_user_wrong_password():
    """
    When I try to login
    And I provide the wrong password
    Then it should 404, not match
    """
    pass


def test_login_user():
    """
    When I try to login
    And I have the right username and a password
    Then it should log me in
    And set the cookie to keep me logged in
    And return the user object
    """
    pass


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
