---
title: Contributor Planning
layout: default
---

At first, there will only be video information with multiple choice questions with textual questions, answers, and feedback. Later stages will add more formats.

Contributor Screens
-------------------

- Dashboard
- Search (Set, Unit, Card...)
- Object Overviews
    - Children, Parents
    - History
- Discussions
    - Proposal

Contributor Models
------------------

### Card

- id
- created
- modified
- language
- unit
- name (e.g. title)
- versioning (canonical)
- tags
- requires
- Videos
    - duration
    - url
- Text Multiple Choice Question
    - question
    - attempts allowed
    - max choices
    - multiple correct
    - answers
        - body
        - correct (boolean)
        - feedback

### Unit

- id
- created
- modified
- language
- versioning (canonical)
- name (title)
- body (objective, goal, description)
- requires

### Set

- id
- created
- modified
- language
- units
- sets
- name
- body (description, objective)
- versioning

### Discussion > Topic

- id
- created
- modified
- language
- entity kind and id
- name

### Discussion > Post

- id
- created
- modified
- language
- user
- topic
- body
- [kind]

### Discussion > Proposal

- Post +
- entity version
- action (create, update, delete ... split, merge)
- status (pending, blocked, accepted, declined)
- name

### Discussion > Vote

- Post +
- proposal
- kind (consent, discuss, dissent)

### Discussion > Flag

- Proposal +
- reason (offensive, irrelevant, incorrect, unpublished, duplicate, inaccessible)

Contributor Endpoints
---------------------


### Card, Unit, Set API

- GET /cards/ (search)
- GET /cards/{id}
- GET /units/ (search)
- GET /units/{id}
- GET /sets/ (search)
- GET /sets/{id}

### Discussion API

- GET /topics/ (search)
- POST /topics/ (create topic)
- PUT (PATCH) /topics/{id} (update topic)
- GET /topics/{id}/posts (list posts)
- POST /topics/{id}/posts (create post, proposal, vote...)
- PUT (PATCH) /topics/{id}/posts/{id} (update post)

### Follow API

- POST /follows/
- DELETE /follows/{id}

Contributor Screen Requirements
-------------------------------

### Object Screen Requirements

The following views are per type: Set, Unit, and Card. These sections list the editable/viewable subcomponents per each type of object.

#### Card Elements

- name
- tags
- requires
- Video:
    - duration and url
- Text Multiple Choice:
    - question
    - answers and feedback
    - options

#### Unit Elements

- name
- goal
- requires

#### Set Elements

- units and sets
- name
- body

--------

### Dashboard

- Notices
    - Subject, time ago, read
- Followed
    - Match search formatting
- My Discussions
    - Topic name, modified, posts
    - My Proposals
        - Name, votes
- Link to search, list views

### Contributor Search (System-wide)

- Search box and button
- No results mode
- Results
    - Infinite scroll
    - Show type (explode out component/integration)
    - Set: name
    - Unit: name
    - Card: name

### List, Search, Filter and Sort View

- Search box and button
- No results mode
- List
    - Infinite scroll
- Order by
    - Latest
    - Watched
    - Proposals
    - Versions
    - Most connections
- Filter by
    - Language
    - ...

#### List Set

- List
    - Show name, body (truncated), contains modules, components (truncated)

#### List Unit

- List
    - Show name, kind, body (truncated), requires (truncated)

#### List Card

- List
    - Video: show name, url (truncated), duration, tags (truncated)
    - Multiple choice text: show body (question, truncated)

### Object View

- Link to discussions/proposals
- Link to history
- Flag it
    - Creates a proposal to delete by system

#### View Set

- See fields above
- List units
- List parent sets

#### View Unit

- See fields above
- List requires
- List required by
- List sets belong to

#### View Card

- See fields above
- Show unit belongs to
- List requires
- List required by

### List History View

- Table layout
    - proposal name
    - proposal time

### Create and Edit Object View

- language (create: select, edit: view)
- Preview edit/create
- Fields: see above
- Unit:
    - Kind selection changes fields available

### Search Discussion Topics

- Search box and button
- Table
    - Topic name
    - Number of posts
    - Last modified
    - Proposals
        - proposal name
        - proposal time
        - status
        - votes

### List Discussion Topics (per Object)

- Same as table for search topics

### Discussion View

- zebra striped cards in list
    - user avatar
    - username
    - date time
    - edited
    - body
    - actions (reply, +1, -1, own: edit)
- infinite scroll
- reverse chronological
- proposal
    - list of proposal blocks and posts
        - Proposal block
            - proposal name
            - proposal body
            - proposal action
            - proposal decision
        - Posts
            - see below
    - Final block
        - Write post
        - Amend proposal (if owned)
        - Vote block (if not owned)
    - Considerations
        - [Contributor Ratings and Proposal Friction](/f_planning/contributor_ratings)

Contributor Wireframes
----------------------

### Components

- Notice post -- Styleguide
- Notices
    - Title
    - 5 latest
    - Link to full page
- Discussion post -- Styleguide
- Proposal post  -- Styleguide
- Vote block  -- Styleguide
- Search (sort, filter) layout -- Styleguide

### Screens

- Dashboard -- TODO
- Search -- TODO
    - Objs
    - Proposals and History
    - Discussion
- View Object -- TODO
- Create/Edit Object -- TODO
- Flag Object -- TODO
- Proposal -- TODO
- Discussion -- TODO
