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


### Contributor Dashboard

- Notifications & Messages
- Watched Objects

### Contributor Search (System-wide)


-------

_Object Screen Requirements_

The following views are per type: Module, Component/Integration, Presentation, and Practice.

### List, Search, Filter and Sort View

#### List Modules
#### List Components & Integrations
#### List Presentations
#### List Practices

### Object View

- List Children & Parents

#### View Module
#### View Component/Integration

- List lost presentation/practice children (?)

#### View Presentation
#### View Practice

### List History View

#### Module History
#### Component/Integration History
#### Presentation History
#### Practice History

### Create and Edit Object View

- Preview edit/create

#### Post Module
#### Post Component/Integration
#### Post Presentation
#### Post Practice

### Proposals View

#### List Module Proposals
#### List Component/Integration Proposals
#### List Presentation Proposals
#### List Practice Proposals

### Proposal View

- Start with something very basic, e.g.
    - 2 points agree, 1 point consent, 0 point discuss, block on dissent
    - 10 points to accept
- Later, list out other factors to consider in formula
    - Age, activity, usage of object
    - Activity and participation of voters
    - Activity and participation of proposer...

#### Module Proposal View
#### Component/Integration Proposal View
#### Presentation Proposal View
#### Practice Proposal View

### Search Discussion Threads

### List Discussion Threads (per Object)

### Discussion View

Contributor Wireframes
----------------------
