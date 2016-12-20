
At first, there will only be video information with multiple choice questions with textual questions, answers, and feedback. Later stages will add more formats.

Contributor Models
------------------

### Card

- id
- created
- modified
- language
- unit
- name (e.g. title)
- versioning (accepted)
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
- versioning (accepted)
- name (title)
- body (objective, goal, description)
- requires

### Set

- id
- created
- modified
- language
- members
- name
- body (description, objective)
- versioning

### Discussion > Topic

- id
- created
- modified
- entity kind and id
- name

### Discussion > Post

- id
- created
- modified
- user
- topic
- body
- [kind]

### Discussion > Proposal

- Post plus...
- entity version
- action (create, update, delete ... split, merge)
- status (pending, blocked, accepted, declined)
- name

### Discussion > Vote

- Post plus...
- proposal
- kind (consent, discuss, dissent)

### Discussion > Flag

- Proposal plus...
- reason (offensive, irrelevant, incorrect, unpublished, duplicate, inaccessible)

Contributor Endpoints
---------------------

### Card, Unit, Set API

- GET `/cards/{id}`
- GET `/units/{id}`
- GET `/sets/{id}`

### Discussion API

- POST `/topics/` (create topic)
- PUT `/topics/{id}` (update topic)
- GET `/topics/{id}/posts` (list posts)
- POST `/topics/{id}/posts` (create post, proposal, vote...)
- PUT `/topics/{id}/posts/{id}` (update post)

### Follow API

- POST `/follows/`
- DELETE `/follows/{id}`

### Search API

- GET `/search/`

Contributor Screen Requirements & Wireframes
--------------------------------------------

### Discussion

- cards in list
    - user avatar
    - username
    - date time
    - body
    - actions (edit, reply, vote, share, flag)
- infinite scroll with pagination
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

<img src="https://docs.google.com/drawings/d/1nIvhNcseLdUu4qzEN_0zfu9QenneynwFgmuDiZp5JC0/pub?w=913&amp;h=1136">

### Create/Edit Topic

- Standard Form Layout
    - Title is one of Create Topic or Edit Topic
- Fields
    - Entity (create: select, edit: view)
    - Name (only editable by original author)
    - plus Fieldset for Create Post if create mode (see below)
- plus Preview Post if create mode

### Create/Edit Post, Proposal, Flag, or Vote

- Standard Form Layout
    - Title updates as kind changes
- Fields
    - Kind (create: select, edit: view)
    - Body
    - Replies to ... (just view, only if applicable)
    - (Hidden: topic)
- Preview
- **Proposal**
    - Name
    - Action
        - If edit entity, select between edit or delete; else just view
    - Status
        - Only on edit and by original poster, allows to decline if applicable
    - **Create/Edit Card**
        - (Card, )Name, Language, Unit, Tags, Requires, Kind
        - Kind selection changes fields available
    - **Create/Edit Unit**
        - (Unit, )Name, Language, Body, Tags, Requires
    - **Create/Edit Set**
        - (Set, )Name, Language, Body, Tags, Members
- **Flag**
    - Reason 'offensive', 'irrelevant', 'incorrect', 'unpublished', 'duplicate', 'inaccessible'
- **Vote**
    - Response (Yes, No)

### Search View

- Search box and button
- No results mode
- List
    - Infinite scroll
- Order by
    - Created
- Filter by
    - Language
    - ...
- Kinds of Entities
    - Set
        - Show name, body (truncated), contains modules, components (truncated)
    - Unit
        - Show name, kind, body (truncated), requires (truncated)
    - Card
        - Video: show name, url (truncated), duration, tags (truncated)
        - Multiple choice text: show body (question, truncated)
        - Show type (explode out card)
    - Topic
        - Topic name
        - Entity name
        - Number of posts
        - Last modified

<img src="https://docs.google.com/drawings/d/1U3EjKczxkUanbjwgLsk81oFJCcJsAMOIR7JJfBdVWxw/pub?w=1440&amp;h=1358">

### View Entity (Template)

- Language
- Name
- Tags
- Flag
- Follow
- Contents (Changes by kind)
- Stats (Changes by kind)
    - Num Learners
    - See [Sequencer](/f_planning/sequencer)
- Relationships (Changes by kind)
- Topics
    - Topic name
    - Number of posts
    - Last modified
- Versions (joins with proposals)
    - Proposal name
    - Created
    - Proposal status (link to pr)
- **Card**
    - Contents
        - Kind Specific Data
            - Video:
                - duration and url
            - Text Multiple Choice:
                - question
                - answers and feedback
                - options
    - Relationships
        - Belongs to (unit)
        - Required By (card)
        - Requires (card)
- **Unit**
    - Contents
        - Body
    - Stats
        - Number of cards > link to search
    - Relationships
        - Requires (unit)
        - Required By (unit)
        - Belongs to (set)
- **Set**
    - Contents
        - Body
        - Members
    - Stats
        - Number of units > link to search
    - Relationships
        - Belongs to (set)

<img src="https://docs.google.com/drawings/d/1S8b5GQnZ2Wj7XPG0cYvS-ac_Syhx6Gcb5lq0gsYUbWk/pub?w=960&amp;h=1920">

<img src="https://docs.google.com/drawings/d/1Q0ymTVBfv_GOk-qDwes0eks3BJGTC1O_p4z_Mq32xjw/pub?w=1440&amp;h=999">

### Follows

- A search view

<img src="https://docs.google.com/drawings/d/17YxWGyu2XO8ndaOQ20KOpwgv5g_EaiCbkaTB73nwwcU/pub?w=1440&amp;h=1034">