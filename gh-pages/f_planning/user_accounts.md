---
title: Account Planning
layout: default
---

This document covers very early planning for the ability for users to create and manage accounts in Sagefy.

Account Screens
---------------

- Home Screen
- Menu
- Login
- Sign Up
- New Password
- Settings
- Terms
- Contact
- Notifications
- Messages

Models
------

### User
- id
- created
- modified
- username
- email
- password
- ip
- notification settings
- roles (array)
- status
- avatar

### Notification
- id
- created
- modified
- name
- body
- tags
- read (boolean)
- concerns: pagination and filtering

### Message
- id
- created
- modified
- from_user
- to_user
- name
- body
- read (boolean)
- tags

Screen Requirements
-------------------

### Home Screen
- Logo and Title
- Short description
- a) Login or Signup
- b) Section selector: Learn, Contribute, Moderate, Mentor, Analyze
- Terms link

### Menu
- Home
- Login/logout
- Settings
- Contact
- Inbox
- Terms

### Login
- Username or email
    - Error
- Password
    - Error
    - I forgot my password
- Login Button
- Create Account link

### Create Account
- Username
    - Validate unique; error
- Email
    - Validate unique; error
- Password
    - Requirements; error
- You agree to TOS
- Create account button
- Login link
- Success: Check inbox, spam, support link; validate email address
    - Then login, Thanks for making account!

### New Password
- Wizard steps
    - 1) Enter email
    - 2) Check inbox
    - 3) Create password
- 1) Email (to confirm you own account), send token button
- 2) Check inbox, few minutes, check spam, support link
- 3) Password field (requirements/errors), update password
    - Then login, notify user of new password

### Settings
- Autosave fields
- Username (validate unique)
- Email (validate unique; errors; warnings; confirm ownership)
- Password => link to create a new password
- Avatar (requirements, errors, etc)
- Notifications settings, for each:
    - Site notification
    - Email
    - Timing (immediate, daily, weekly...)

### Terms
- List terms and privacy policy

### Contact
- List methods of contact

### Inbox (Messages and Notifications)
- List notifications
    - Filter notifications by type
    - Each notification:
        - Image
        - Subject
        - Body
        - Action
        - Seen/unseen status
        - Time ago
- Unread messages
    - Time ago
    - From
    - Subject
- All messages
    - Time ago
    - From
    - Subject
    - Unread/read status
- Sent messages
    - Time ago
    - From
    - Subject
- View message
    - From, To
    - Subject
    - Body
    - Reply to message
- Create message
    - To
    - Subject
    - Body
    - Send

Wireframes
----------

### Home

![s](https://docs.google.com/drawings/d/1pmBonQ3RMj0KNDoNbtYc1DlevFesU-ccVfWSQURS_jg/pub?w=600&amp;h=600)

### Home, Logged In

![s](https://docs.google.com/drawings/d/1xKI3bG41ciyb_YPhkS6nYTkK4nusl8cPfsDpAp3N5oY/pub?w=600&amp;h=600)

### Menu

![s](https://docs.google.com/drawings/d/1OdmkO8ND2wdbql3y-K787xEJFa5-EV3CemWg7PJJN-E/pub?w=600&amp;h=600)

### Create Account

![s](https://docs.google.com/drawings/d/1WSzws0D3ZMaYTQqJmzNJAJcmpl91XT1ii9w4BkPAEzg/pub?w=600&amp;h=600)

### Reset Password

![s](https://docs.google.com/drawings/d/1p88C-Am9LHNyirPBcsUEZ195s04uo3IiK-3J5coL9EA/pub?w=600&amp;h=600)

### Settings

![s](https://docs.google.com/drawings/d/1EWBadWBpQCfXXcFrH9D1--h8cb2dMFDljSH1SfVw2TY/pub?w=600&amp;h=600)

### Messages

![s](https://docs.google.com/drawings/d/1Tf6oDRukTVWBYi9nZnNyOGKjaB4J1vyjAT65IUN1Gmo/pub?w=600&amp;h=600)

### Notifications

![s](https://docs.google.com/drawings/d/1wC5h3JBFLG4ALnxVkT_RocjcifuqmfWoy8Cx8hy1fxM/pub?w=600&amp;h=600)
