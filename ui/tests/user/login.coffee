
###
Given I am on the login page
When I submit without a username or password
Then I should see errors on the form
###

###
Given I am on the login page
When I enter the wrong password
Then I should see an error
###

###
Given I am on the login page
When I enter correct login information
Then I am logged in
And redirected to the dashboard
###
