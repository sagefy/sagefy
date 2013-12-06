Account Planning
================

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
- type
- user_id
- object_id
- object_type
- subject
- body
- action
- action_url
- seen

### Message
- id
- created
- modified
- type
- format
- from_user_id
- to_user_id
- subject
- body
- read

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
    - => Then login, Thanks for making account!

### New Password
- Wizard steps
    - 1) Enter email
    - 2) Check inbox
    - 3) Create password
- 1) Email (to confirm you own account), send token button
- 2) Check inbox, few minutes, check spam, support link
- 3) Password field (requirements/errors), update password
    - => Then login, notify user of new password

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
![Home](https://dl.dropboxusercontent.com/u/178965380/wireframes/home.png)

### Home, Select
![Home, Select](https://dl.dropboxusercontent.com/u/178965380/wireframes/home_select.png)

### Menu
![Menu](https://dl.dropboxusercontent.com/u/178965380/wireframes/menu.png)

### Login
![Login](https://dl.dropboxusercontent.com/u/178965380/wireframes/login.png)

### Create Account
![Create Account](https://dl.dropboxusercontent.com/u/178965380/wireframes/create_account.png)

### New Password
![New Password](https://dl.dropboxusercontent.com/u/178965380/wireframes/new_password.png)

### Settings
![Settings](https://dl.dropboxusercontent.com/u/178965380/wireframes/settings.png)

### Inbox
![Inbox](https://dl.dropboxusercontent.com/u/178965380/wireframes/inbox.png)