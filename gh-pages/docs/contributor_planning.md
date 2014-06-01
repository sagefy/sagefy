---
title: Contributor Planning
layout: default
---

At first, there will only be video information with multiple choice questions with textual questions, answers, and feedback. Later stages will add more formats.

Contributor Screens
-------------------

- Section Selector
- Contributor Home
- Contributor Search (Modules, Components, Information...)
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

- _Versioning_
- _Internationalization and Translation_
- _Notifications_
- _Flagging_
- _Discussion_

### Module
- id
- created
- modified
- version
- name (aka title, topic, subject)
- body (aka description)
- component_ids (array)
- module_ids (array)
    - !! ensure no prereq cycles

### Component (or Integration)
- id
- created
- modified
- version
- name (aka title, topic, subject)
- body (aka description)
- prerequisite_ids (array)
    - !! ensure no prereq cycles
- type (component, integration)
    - !! ensure integration has no learning objectives

### Learning Objective
- id
- created
- modified
- version
- component_id
- body (aka copy, text)
    - languages (en, es, jp)
- ordinal (order)

### Information
- id
- component_id
- version
- created
- modified
- format_type
- format_id
- learning_objective_id
- categories (eg worked example, application, motivational, compare and contrast...)
- language

#### Information: Video Format
- id
- parent_id
- duration
- url

### Practice
- id
- component_id
- version
- created
- modified
- learning_objective_id
- language
- question_id
- question_type
- answer_id
- answer_type

### Practice: Question > Textual
- id
- practice_id
- created
- attempts_allowed
- modified
- question

### Practice: Answer > Selection
- id
- practice_id
- created
- modified
- answers
    - formats
    - correct_answer
    - feedback
- single_or_multiple

### Proposal
- id
- created
- modified
- object_id
- object_type
- name (aka title, subject)
- body (description)

### Proposal: Versions (Amendments)
- id
- created
- modified
- version (based on)
- proposal_id
- status (active, pending, accepted, declined, can't accept)
- name
- body
- type (create, update, delete, split, merge)
- fields

### Proposal: Votes
- id
- created
- modified
- user_id
- proposal_version_id
- type (agree, consent, discuss, disagree...)

### Discussion > Thread
- id
- created
- modified
- object_id
- object_type
- name

### Discussion > Message
- id
- created
- modified
- user_id
- body (aka message, copy)
- reply_to (message_id)
- thread_id

Contributor Screen Requirements
-------------------------------

### Object Screen Requirements

The following views are per type: Module, Component/Integration, Presentation, and Practice.

These sections list the editable/viewable subcomponents per each type of object.

#### Module Elements

- language
- name (title)
- body (description)
- contains
    - modules
    - components

#### Component/Integration Elements

- language
- name (title)
- body (description)
- objectives (listed, ordered)
- changes depending on being either component or integration
    - kind
    - prerequisites
        - Component has zero to many prerequisites, must only be other components
        - Integration must have exactly two prerequisites of either type

#### Presentation Elements

- language
- kind
- objective belongs to
- video specific:
    - name
    - url
    - duration
- categories

#### Practice Elements

- language
- kind
- objective belongs to
- multiple choice text
    - attempts allowed
    - max choices
    - multiple correct (boolean)
    - body (question)
    - answer
        - body (text)
        - correct (boolean)
        - feedback (text)
- categories

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
    - Module: name
    - Component: name
    - Presentation::Video: name
    - Practice::Multiple Choice::Text: body (question) ... truncated

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

#### List Modules

- List
    - Show name, body (truncated), contains modules, components (truncated)

#### List Components & Integrations

- List
    - Show name, kind, body (truncated), prereqs (truncated)

#### List Presentations

- List
    - Video: show name, url (truncated), duration, categories (truncated)

#### List Practices

- List
    - Multiple choice text: show body (question, truncated)

### Object View

- Link to discussion
- Link to history
- Link to proposals
- Flag it
    - Creates a proposal to delete by system

#### View Module

- See fields above
- List element modules and components
- List parent modules

#### View Component/Integration

- See fields above
- List prerequisites
- List prerequisite ofs
- List modules belong to
- List lost presentation/practice children (?)

#### View Presentation

- See fields above
- Show objective belongs to, component/integration belongs to

#### View Practice

- See fields above
- Show objective belongs to, component/integration belongs to

### List History View

- Table layout
    - proposal name
    - proposal time

### Create and Edit Object View

- language (create: select, edit: view)
- Preview edit/create
- Fields: see above
- Presentation/Practice:
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
