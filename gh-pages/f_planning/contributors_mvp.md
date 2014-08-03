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

- TODO

### Unit

- TODO

### Set

- TODO

### Proposal

- TODO

### Vote

- TODO

### Discussion > Thread

- TODO

### Discussion > Message

- TODO

Contributor Screen Requirements
-------------------------------

### Object Screen Requirements

The following views are per type: Set, Unit, and Card. These sections list the editable/viewable subcomponents per each type of object.

#### Set Elements

- TODO

#### Unit Elements

- TODO

#### Card Elements

- TODO
- Video: TODO
- Text Multiple Choice: TODO

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
