# When I get a user
# And I'm not that user
# Then I should not get their email or password

# When I get a user
# And I am that user
# Then I should get the email, but not the password

# When I get a user by ID
# And no user exists by that ID
# Then I should get an empty response

# When I get a user by ID
# And a user exists for that ID
# Then I should get a user
