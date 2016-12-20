---
layout: docs
title: Planning> User Accounts
---

This document covers very early planning for the ability for users to create and manage accounts in Sagefy.

Account Screens
---------------

- Home Screen
- Menu
- Log In
- Sign Up
- New Password
- Settings
- Terms
- Contact
- Notices

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
- notice settings
- roles (array)
- status
- avatar

### Notice
- id
- created
- modified
- name
- body
- tags
- read (boolean)
- concerns: pagination and filtering

Screen Requirements
-------------------

### Home Screen
- Logo and Title
- Short description
- Log In or Sign Up
- Terms link

### Menu
- Home
- Log In/Log Out
- Settings
- Contact
- Inbox
- Terms

### Log In
- Username or email
    - Error
- Password
    - Error
    - I forgot my password
- Log In Button
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
- Log In link
- Success: Check inbox, spam, support link; validate email address
    - Then log in, Thanks for making account!

### New Password
- Wizard steps
    - 1) Enter email
    - 2) Check inbox
    - 3) Create password
- 1) Email (to confirm you own account), send token button
- 2) Check inbox, few minutes, check spam, support link
- 3) Password field (requirements/errors), update password
    - Then log in, notify user of new password

### Settings
- Autosave fields
- Username (validate unique)
- Email (validate unique; errors; warnings; confirm ownership)
- Password => link to create a new password
- Avatar (requirements, errors, etc)
- Notices settings, for each:
    - Site notice
    - Email
    - Timing (immediate, daily, weekly...)

### Terms
- List terms and privacy policy

### Contact
- List methods of contact

### Inbox (Notices)
- List notices
    - Filter notices by type
    - Each notice:
        - Image
        - Subject
        - Body
        - Action
        - Seen/unseen status
        - Time ago

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

### Notices

![s](https://docs.google.com/drawings/d/1wC5h3JBFLG4ALnxVkT_RocjcifuqmfWoy8Cx8hy1fxM/pub?w=600&amp;h=600)
