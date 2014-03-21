
# When I instantiate a user with a valid username, email, and password
# Then I should get a valid user object
# And the user should be stored in the database
# And the password should be encrypted in the database

# When I create a new user
# And the username isn't set
# Then it should assert an error

# When I create a new user
# And the username already exists in the system
# Then it should assert an error

# When I create a new user
# And the email address isn't set
# Then it should assert an error

# When I create a new user
# And the email address isn't an email address
# Then it should assert an error

# When I create a new user
# And the email already exists in the system
# Then it should assert an error

# When I create a new user
# And the password isn't set
# Then it should assert an error

# When I create a new user
# And the password is less than 8 characters long
# Then it should assert an error

# When I create a new user
# And the password doesn't contain a number
# Then it should assert an error

# When I create a new user
# And the password doesn't contain an uppercase letter
# Then it should assert an error

# When I create a new user
# And the password contains the username or email
# Then it should assert an error

# When I create a new user
# And the password is very common
# Then it should assert an error

# When I create a new user by hitting the API
# Then I should get a user JSON

# When I try to create a new user by hitting the API
# And I provide problematic information
# Then I should get an error JSON
