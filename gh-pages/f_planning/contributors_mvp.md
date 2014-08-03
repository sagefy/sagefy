---
title: Contributor Planning
layout: default
---

At first, there will only be video information with multiple choice questions with textual questions, answers, and feedback. Later stages will add more formats.

Contributor Screens
-------------------

- Section Selector
- Contributor Home
- Contributor Search (Set, Unit, Card...)
- Object Overviews
    - Children, Parents
    - History
    - List Proposals
    - Discussions
- Proposal
    - Create
    - Amend
    - Agree, Consent, Discuss, Dissent...

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
- categories
- prerequisites
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
- prerequisites

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

### Proposal

- id
- created
- modified
- language
- user
- object kind, id

### Amendments

- id
- created
- modified
- language
- proposal
- object version
- action (create, update, delete, split, merge)
- decision (pending, blocked, accepted, declined)

### Vote

- id
- created
- modified
- language
- user
- amendment
- body
- action (agree, consent, discuss, dissent)

### Discussion > Thread

- id
- created
- modified
- language
- object kind and id
- name

### Discussion > Message

- id
- created
- modified
- language
- user
- thread
- body
- replies to message

Contributor Screen Requirements
-------------------------------

### Object Screen Requirements

The following views are per type: Set, Unit, and Card. These sections list the editable/viewable subcomponents per each type of object.

#### Card Elements

- name
- categories
- prerequisites
- Video:
    - duration and url
- Text Multiple Choice:
    - question
    - answers and feedback
    - options

#### Unit Elements

- name
- goal
- prerequisites

#### Set Elements

- units and sets
- name
- body

--------

### Contributor Dashboard

- Notifications
    - Subject, time ago, read
- Messages
    - From, subject, time ago, read
- Watched
    - Match search formatting
- My Proposals
    - Name, votes
- My Discussions
    - Thread name, modified, messages
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
    - Show name, kind, body (truncated), prereqs (truncated)

#### List Card

- List
    - Video: show name, url (truncated), duration, categories (truncated)
    - Multiple choice text: show body (question, truncated)

### Object View

- Link to discussion
- Link to history
- Link to proposals
- Flag it
    - Creates a proposal to delete by system

#### View Set

- See fields above
- List units
- List parent sets

#### View Unit

- See fields above
- List prerequisites
- List prerequisite ofs
- List sets belong to

#### View Card

- See fields above
- Show unit belongs to
- List prerequisites
- List prerequisite ofs

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

### Proposals View

- object summary
- list
    - proposal name
    - proposal time
    - status
    - votes

### Proposal View

- list of proposal blocks and messages
    - Proposal block
        - proposal name
        - proposal body
        - proposal action
        - proposal decision
    - Messages
        - see below
- Final block
    - Write message
    - Amend proposal (if owned)
    - Vote block (if not owned)
- Considerations
    - Start with something very basic, e.g.
        - 2 points agree, 1 point consent, 0 point discuss, block on dissent
        - 10 points to accept
    - Later, list out other factors to consider in formula
        - Age, activity, usage of object
        - Activity and participation of voters
        - Activity and participation of proposer...

### Search Discussion Threads

- Search box and button
- Table
    - Thread name
    - Number of messages
    - Last modified

### List Discussion Threads (per Object)

- Same as table for search threads

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


Contributor Wireframes
----------------------

TODO
