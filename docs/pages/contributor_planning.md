Contributor Planning
====================

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
- type (create, update, delete, split, merge)
- fields (changes, updates)
- status (active, pending, accepted, declined, can't accept)
- version (based on)

### Proposal: Votes
- id
- created
- modified
- user_id
- object_id
- object_id
- type (agree, consent, discuss, disagree...)

### Proposal: Amendments
- id
- created
- modified
- proposal_id
- status
- name
- body
- type
- fields

### Discussion > Thread
- id
- created
- modified
- object_id
- object_type
- name
- body (aka description)

### Discussion > Message
- id
- created
- modified
- user_id
- object_id
- object_type
- body (aka message, copy)
- reply_to (message_id)
- thread_id

Contributor Screen Requirements
-------------------------------

### Section Selector
- Logo
- Links to sections: Learn, Contribute...
- Menu

### Contributor Home

### Contributor Search (Modules, Components, Information...)

### Object Overviews
- Children, Parents
- History
- List Proposals
- Discussions
- -
- Create Component
    - Five to eight minutes of information, 30-60 minutes of practice to bronze
- Create/Edit Learning Objectives
    - Three to five learning objectives
    - Allow subjectives
    - Reordering

### View Proposal
- Agree, Consent, Discuss, Dissent...

### Create Proposal

### Amend Proposal

Contributor Wireframes
----------------------
