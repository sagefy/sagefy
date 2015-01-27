---
layout: default
title: Sagefy Web API
---

This document outlines the endpoints for Sagefy and their specifications.

Errors will appear in the following format, along with the appropriate status code (400, 401, 403, 404):

```json
{
    "errors": [{
        "name": "field",
        "message": "The reason for the error."
    }]
}
```

Here I use _Request Parameters_ for GET and DELETE and _Request Format_ for POST, PATCH, and PUT.

Public
======

Welcome
-------

`GET https://sagefy.org/api/`

### Request Parameters

None

### Response Format

```json
{
    "message": "Welcome to Sagefy."
}
```

Users
=====

Get User By ID
--------------

`GET https://sagefy.org/api/users/{id}/`

Get the user information given a user ID.

### Request Parameters

None

### Response Format (200)

```json
{
    "user": {
        "name": "test",
        "email": "test@example.com",
        "email_frequency": "immediate"
    }
}
```

`email` and `email_frequency` are private and only available to the self user.

Returns a 404 if user is not found.

Get Current User
----------------

`GET https://sagefy.org/api/users/current/`

Get the current user's information, if available.

### Request Parameters

None

### Response Format (200)

```json
{
    "user": {
        "name": "test",
        "email": "test@example.com",
        "email_frequency": "immediate"
    }
}
```

`email` and `email_frequency` are private and only available to the self user.

Returns a 401 if a user is not logged in.

Create User
-----------

`POST https://sagefy.org/api/users/`

### Request Format

```json
{
    "name": "test",
    "email": "test@example.com",
    "password": "abcd1234"
}
```

### Response Format (200)

```json
{
    "user": {
        "name": "test",
        "email": "test@example.com",
        "email_frequency": "immediate"
    }
}
```

Returns a 400 if there are errors, such as email already used or password too short.

Login User
----------

`POST https://sagefy.org/api/users/login/`

### Request Format

```json
{
    "name": "test",
    "password": "abcd1234"
}
```

### Response Format (200)

```json
{
    "user": {
        "name": "test",
        "email": "test@example.com",
        "email_frequency": "immediate"
    }
}
```

Returns 404 if the user by name is not found. Returns a 400 if the password is not valid.

Logout User
-----------

`POST https://sagefy.org/api/users/logout/`

### Request Format

None

### Response Format (204)

None

Update User
-----------

Create Password Token
---------------------

Create Password
---------------

Get User Menu
-------------

Get User Sets
-------------

Add User Set
------------

Remove User Set
---------------

Cards
=====

Get Card Information
--------------------

Render Card for Learner
-----------------------

Respond to Card
---------------

Units
=====

Get Unit Information
--------------------

Sets
====

Get Set Information
-------------------

Get Set Tree
------------

Show Available Units from Set
-----------------------------

Choose Unit
-----------

Sequencer
=========

Next
----

Search
======

Search
------

Topic
=====

Create Topic
------------

Update Topic Name
-----------------

Get Posts
---------

Create Post
-----------

Update Post
-----------

Follow
======

Follow
------

Unfollow
--------

Notices
=======

List Notices
------------

Mark Notice as Read
-------------------

Mark Notice as Unread
---------------------
