
FORMAT: 1A
HOST: http://sagefy.org/

# Sagefy Web Service API

This document outlines the endpoints for Sagefy and their specifications.

Errors will appear in the following format, along with the appropriate status code (400, 401, 403, 404):

        {
            "errors": [{
                "name": "field",
                "message": "The reason for the error."
            }]
        }

## Welcome [/s]

### Welcome Message [GET]

Welcomes the developer to the Sagefy service.

+ Response 200 (application/json)

        {
            "message": "Welcome to Sagefy."
        }

## Users [/s/users]

### Create a new user [POST]

Create a new user account.

Returns a 400 if there are errors, such as email already used or password too short.

+ Request (application/json)

        {
            "name": "test",
            "email": "test@example.com",
            "password": "abcd1234"
        }

+ Response 200 (application/json)

        {
            "user": {
                "name": "test",
                "email": "test@example.com",
                "email_frequency": "immediate"
            }
        }

## User [/s/users/{id}]

### Get a user [GET]

Get the user information given a user ID.

`email` and `email_frequency` are private and only available to the self user.

Returns a 404 if user is not found.

`current` may be substituted for `id`. In that case, returns a 401 if a user is not logged in.

+ Response 200 (application/json)

        {
            "user": {
                "name": "test",
                "email": "test@example.com",
                "email_frequency": "immediate"
            }
        }

### Update a user [PUT]

Update the user. Must be the current user.

Return a 404 if no user matching that ID. Return 401 if not the current user. Return 400 for parameter issues.

+ Request (application/json)

        {
            "name": "test",
            "email": "test@example.com",
            "password": "abcd1234"
        }

+ Response 200 (application/json)

        {
            "user": {
                "name": "test",
                "email": "test@example.com",
                "email_frequency": "immediate"
            }
        }

## Log in or out user [/s/sessions]

### Log in as user [POST]

Log in as an existing user.

Returns 404 if the user by name is not found. Returns a 400 if the password is not valid.

+ Request (application/json)

        {
            "name": "test",
            "password": "abcd1234"
        }

+ Response 200 (application/json)

        {
            "user": {
                "name": "test",
                "email": "test@example.com",
                "email_frequency": "immediate"
            }
        }

### Log out as user [DELETE]

Log out of the current user.

+ Response 204

## Password Token [/s/password_tokens]

### Create Password Token [POST]

Email a token to be able to reset the password.

Return a 404 if it cannot find the user's email.

+ Request (application/json)

        {
            "email": "test@example.com"
        }

+ Response 204 (application/json)

## Create Password [/s/users/{user_id}/password]

### Create a password [POST]

Update the user's password. Must have a matching and timely token.

200 also logs in user. 404 if not a valid user ID. 403 if the token doesn't match.

+ Request (application/json)

        {
            "id": "ABCD1234",
            "token": "JFDN32JL29af",
            "password": "abcd1234"
        }

+ Response 200 (application/json)

        {
            "user": {
                "name": "test",
                "email": "test@example.com",
                "email_frequency": "immediate"
            }
        }

## User Sets [/s/users/{id}/sets]

### Get all of users' sets [GET]

Get the list of learner's sets.

401 if not logged in. 403 if not current user.

+ Response 200 (application/json)

        {
            "user_id": "fnsLJIoel",
            "set_ids": ["fjkOTJRLEf"]
        }

## User Set [/s/users/{id}/sets/{id}]

### Add a user set [POST]

Add a set to the learner's list.

401 if not logged in. 403 if not current user. 404 if set not found. 409 if already added.

+ Response 200 (application/json)

        {
            "user_id": "fnsLJIoel",
            "set_ids": ["fjkOTJRLEf"]
        }

### Remove a user set [DELETE]

Remove a set from the learner's list.

401 if not logged in. 403 if not current user. 404 if set not found.

+ Response 200 (application/json)

        {
            "user_id": "fnsLJIoel",
            "set_ids": ["fjkOTJRLEf"]
        }

### Select a user set [PUT]

Selects a set for the user to engage.

+ Response 200

## Card [/s/cards/{id}]

Cards are the smallest entity in the Sagefy data structure system. A card represents a single learner activity.

### Get card [GET]

Get a specific card given an ID. Show all relevant data, but
not used for the learning interface.

Always returns the latest accepted version. 404 if card not found.

+ Response 200 (application/json)

        {
            "card": {
                "name": "Lorem ipsum.",
                "body": "Lorem ipsum.",
                "options": [{
                    "body": "Details...",
                    "correct": false
                }]
            }
        }

## Card for Learning [/s/cards/{id}/learn]

Some data is filtered out, such as feedback and which answer is correct.

### Get card [GET]

Render the card's data, ready for learning.

+ Response 200 (application/json)

        {
            "card": {
                "name": "Lorem ipsum.",
                "body": "Lorem ipsum.",
                "options": [{
                    "body": "Details..."
                }]
            }
        }

## Card Responses [/s/cards/{id}/responses]

### Create a card response [POST]

Record and process a learner's response to a card.

+ Request

        {
            "card_id": "zFK2201",
            "response": 3
        }

+ Response 200

        {
            "response": {
                "user_id": "Fj2Fo3L",
                "card_id": "zFK2201",
                "unit_id": "Y2o081l",
                "score": 1
            }
        }

## Card Versions [/s/cards/{card_id}/versions]

### Get card versions [GET]

+ Response 200

## Unit [/s/units/{id}]

A unit is the medium size in the Sagefy data structure system. A unit represents a unit of learning activity.

### Get unit info [GET]

Get a specific unit given an ID.

Always returns the latest accepted version. 404 if card not found.

+ Response 200

        {
            "unit": {
                "language": "en",
                "name": "Lorem ipsum.",
                "body": "Lorem ipsum.",
                "tags": ["analyze"],
                "require_ids": ["a5kJ3kj"]
            }
        }

## Unit Versions [/s/units/{unit_id}/versions]

### Get unit versions [GET]

+ Response 200

## Set [/s/sets/{id}]

A set is a collection of units and other sets.

### Get set information [GET]

Get a specific set given an ID.

+ Response 200

        {
            "set": {
                "language": "en",
                "name": "Lorem ipsum.",
                "body": "Lorem ipsum.",
                "tags": ["Y950fnNo"],
                "members": [{
                    "id": "9JmFKI04",
                    "kind": "unit"
                }]
            }
        }

## Set Versions [/s/sets/{set_id}/versions]

### Get set versions [GET]

+ Response 200

## Set Tree [/s/sets/{id}/tree]

### Get set tree [GET]

Render the tree of units that exists within a set.

404 if set not found.

+ Response 200

        {
            "units": {
                "fRjglO0": ["59JkflsoT", "Jn34NFKo0"]
            }
        }

## Set' Units [/s/sets/{id}/units]

### Get set units [GET]

Render the units that exist within the set.

Specifically, present a small number of units the learner can choose from.

401 if not logged in. 404 if set not found. 400 if it doesn't make sense.

+ Response 200

        {
            "units": [{
                "language": "en",
                "name": "Lorem ipsum.",
                "body": "Lorem ipsum.",
                "tags": ["analyze"],
                "require_ids": ["a5kJ3kj"]
            }]
        }

## Set' Unit [/s/sets/{id}/units/{id}]

### Choose unit [POST]

Updates the learner's information based on the unit they have chosen.

401 if not logged in. 404 if set or unit not found. 400 if it doesn't make sense.

+ Response 204

## Next [/s/next]

Next is an abstract resource which only determines one thing: where to go next.

### Next [GET]

Tell the learner where to go next.

Can lead to a card, tree, or choose unit screen.

+ Response 200

        {
            "kind": "card",
            "card_id": "aFN03O2m"
        }

## Search [/s/search]

Site-wide search for cards, units, sets, users, topics, and posts.

### Search [GET]

Search for entities.

+ Parameters
    + q (optional) - Text index based search query.
    + skip (optional) - Offset results by count.
    + limit (optional) - Maximum number of results to return.
    + order
    + kind (optional) - the kind of entity to search for (e.g. set, card, unit)
    + as_learner (optional)

+ Response 200

        {
            "results": [{
                {
                    "table": "card",
                }
            }]
        }

## Topics [/s/topics]

Topics, or threads, are the entity that hold a conversation, a list of posts. The Topic service handles both topics and posts, as posts always belong to a single topic.

### Create topic [POST]

Create a new topic. The first post (proposal, flag) must be provided.
Flag: if a flag for the same reason exists for the entity, create a vote there instead.

When creating a topic, you must also submit information for a valid post. There are four post kinds. All require the "kind" field filled out. Replies to ID is optional. Proposals also require an entity version ID, name, status, and action. Votes have optional bodies, but require "replies_to_id" and "response". Flag requires entity version ID, name, reason, and status.

Returns 400 if missing or invalid topic or post information. Return 401 if not logged in as a user.

+ Request

        {
            "topic": {
                "name": "Lorem ipsum.",
                "entity": {
                    "kind": "card",
                    "id": "fj204lasZ"
                }
            },
            "post": {
                "body": "Lorem ipsum.",
                "kind": "post",
                "replies_to_id": "a42lf9"
            }
        }

+ Response 200

        {
            "topic": {
                "id": "fjkls234",
                "name": "Lorem ipsum.",
                "entity": {
                    "kind": "card",
                    "id": "fj204lasZ"
                }
            },
            "post": {
                "user_id": "ajfkl234",
                "body": "Lorem ipsum.",
                "kind": "post",
                "replies_to_id": "a42lf9",
                "topic_id": "fjkls234"
            }
        }

## Topic [/s/topics/{id}]

### Update topic [PUT]

Update the topic. Only the name can be changed. Only by original author.

401 if not logged in. 404 if topic by ID not found. 403 if not user's own topic. 400 if there's issues with the name field.

+ Request

        {
            "name": "Neo name."
        }

+ Response 200

        {
            "topic": {
                "id": "fjkls234",
                "name": "Neo name.",
                "entity": {
                    "kind": "card",
                    "id": "fj204lasZ"
                }
            }
        }

## Posts [/s/topics/{id}/posts]

### Get posts [GET]

Get a reverse chronological listing of posts for given topic.
Includes topic meta data and posts (proposals, votes, flags).
Paginates.

Returns 404 if topic not found. Posts can be one of post, proposal, vote, or flag. The kind changes the field available.

+ Parameters
    + skip - Maximum number of posts to return.
    + limit - Offset the return by count.

+ Response 200

        {
            "posts": [{
                "user_id": "ajfkl234",
                "body": "Lorem ipsum.",
                "kind": "post",
                "replies_to_id": "a42lf9",
                "topic_id": "fjkls234"
            }]
        }

### Create post [POST]

Create a new post on a given topic.
Accounts for posts, proposals, votes, and flags.
Proposal: must include entity (card, unit, set) information.
Vote: must refer to a proposal.

401 if not logged in. 404 if topic not found. 400 if issue presented with content.

+ Request

        {
            "body": "Lorem ipsum.",
            "kind": "post",
            "replies_to_id": "a42lf9"
        }

+ Response 200

        {
            "user_id": "ajfkl234",
            "body": "Lorem ipsum.",
            "kind": "post",
            "replies_to_id": "a42lf9",
            "topic_id": "fjkls234"
        }

## Post [/s/topics/{id}/post/{id}]

### Update post [PUT]

Update an existing post. Must be one's own post.
For proposals:
The only field that can be updated is the status;
the status can only be changed to declined, and only when
the current status is pending or blocked.

401 if not logged in. 403 if not own post. 400 if issues with content.

+ Request

        {
            "body": "Neo body."
        }

+ Response 200

        {
            "user_id": "ajfkl234",
            "body": "Neo body.",
            "kind": "post",
            "replies_to_id": "a42lf9",
            "topic_id": "fjkls234"
        }

## Follows [/s/follows]

Follows allow users to subscribe to updates on cards, units, and sets.

### List follows [GET]

+ Response 200

### Follow [POST]

Current user follows an entity, topic, or proposal.

Return 401 if not logged in. Return 400 if content issues.


+ Request

        {
            "entity": {
                "kind": "card",
                "id": "fjk20tnJF"
            }
        }

+ Response 200

        {
            "user_id": "abcd1234",
            "entity": {
                "kind": "card",
                "id": "fjk20tnJF"
            }
        }

## Follow [/s/follows/{id}]

### Unfollow [DELETE]

Remove a follow. Must be current user's own follow.

Return 404 if it doesn't find that follow. Return 401 if not logged in. Return 403 if not own follow. Return 400 if other errors.

+ Response 204

## Notices [/s/notices]

Notices provide updates to users on cards, units, and sets they follow.

### List notices [GET]

List notices for current user.

Returns a 401 if there's no user currently logged in.

+ Parameters
    + limit - Maximum number of notices to return.
    + skip - Offset in returned set.
    + tag - Filter by a specific tag.
    + read - Filter by read or unread notices.

+ Response 200

        {
            "notices": [{
                "id": "abcd1234",
                "user_id": "fjskl234",
                "kind": "create_proposal",
                "read": false,
                "tags": ["analyze"]
            }]
        }

## Notice [/s/notices/{id}]

### Mark notice as read/unread [PUT]

Mark notice as read.
Must be logged in as user, provide a valid ID, and own the notice.
Return notice.

Returns 401 if not logged in. Returns 404 if notice not found. Returns 403 if not user's own notice. Returns 400 if issues saving to the database.

+ Response 200

        {
            "notice": {
                "id": "abcd1234",
                "user_id": "fjskl234",
                "kind": "create_proposal",
                "read": false,
                "tags": ["analyze"]
            }
        }
