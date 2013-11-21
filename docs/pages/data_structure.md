Data Structure
==============

This document covers the overall architecture of Descovrir's data storage. This data structure allows Descovrir to be both open-content as well as highly adaptive and flexible while maintaining practicality.

![data structure](https://dl.dropboxusercontent.com/u/178965380/data_structure.png)

Overview
--------

- Component
    - Objectives
    - Information
    - Practice
    - Application
    - Relationships
- Integration
    - Information
    - Practice
    - Application
    - Relationships
-  Module
    - Composition
    - Application

Components
----------

- A small learning lesson, may contain about five to eight minutes of information and 30-60 minutes of practice to gain proficiency
- **Learning objectives**
    - Three to five statements that indicate information, practice, and assessment to include.
    - Can be reordered.
    - Subobjectives are allowed.
    - Displayed to the learner at the beginning of the component, can be reviewed at any time.
- **Information**
    - Formatting:
        - Text
        - Audio
        - Slideshow
        - Slideshow with Audio
        - Video
        - Interactive
        - Timeline
    - Question interjection in each format to assess comprehension
    - Multiple per component: languages, formats, approaches
    - Additional types of information presentation:
        - Worked examples
        - Application examples
        - Motivational examples
        - Compare and contrast
- **Practice**
    - Contains question, answer, and feedback
    - Can be tied to a learning objective.
    - Question
        - Text
        - Image
        - Audio
        - Video
        - Interactive
    - Answer
        - True or False
        - Radio (Multiple choice, one answer)
            - Randomize order
            - Randomize availability
            - Allow for multiple choice, true/false questions
        - Checkbox (Multiple choice, multiple answers)
            - Same as radio properties
            - 'All that apply' questions
        - Number
        - Time or date
        - Short text
        - Multiple short text
        - Matching
        - Matrix
            - A table of rows and columns
            - Can select radio, checkbox, number, time date or short text per rows or per columns
        - Textarea
        - File upload
            - Audio (microphone?)
            - Video (built in camera?)
            - Image
            - Document (PDF, txt, code...)
        - Interactive
            - Evaluated by function or peer review
    - Feedback
        - Tied to answer format
        - Radio, checkbox, number, time, date, short text
            - Immediate feedback
            - Specify number of attempts before giving and explaining answer
        - Short text
            - Set length, regex match
        - Textarea, file upload
            - Peer review
                - Provide rubrics for evaluation.
                - Allow for textual feedback in addition to numeric.
            - Craftier solutions (regex, NLP, signal analysis...)
        - Interactive
            - Programatically evaluated
            - Open peer review API to interface evaluation
    - _Practice Set_
        - A short series of questions that should be kept together and in order.
- **Application** (Projects)
    - Individual, collaborative, or team.
    - Basic layout:
        - **Propose**: Provide the learner with a description of the task.
        - **Assess**: Assess the learner's understanding of the task.
        - **Plan**: Ask the learner to evaluate the task, break it into parts, and form a plan.
        - **Action**: Have learner implement their plan.
        - **Review**: Have the learner evaluate other's work on the same task.
        - **Result**: Invite learner to review own work against peer reviews.
        - **Reflect**: Invite learner to reflection on project experience and discuss and rate application project quality.
    - Not all steps are required.
    - Proposal, analysis, evaluation, review, and reflection can all use practice question formats.
    - Action can also use practice question formats.
    - Rubrics system: provide a systematic means of evaluation.
    - Encourage creation of both short and longer application projects. (10 minutes - 2-3 hours)
- **Relationships**
    - Prerequisites
        - Can list components or modules that are required before addressing component
        - Prefer specificity in prerequisites over shotgun approaches: what does the learner really need to know to begin this specific component?
        - AND and OR operators on prerequisites?

Integrations
------------

- Defined as a relationship between
    - Two components
    - A component and an integration
    - Two integrations
- Contains information, practice, and application
- Does **not** contain new learning objectives.

Modules
-------

- Defined by a set of components and other modules
- Describes larger sets of goals and objectives, such as American Sign Language or Japanese Art History
- May contain own application units that would require most or all of the components in the set.

*More notes*
- Add language and geographic tags to information, practice, etc
- Add translations for learning objectives

* * *

User-based Requirements
-----------------------

- **Learning Objectives**
    - _Learners_
        - See objectives in my language
    - _Contributors_
        - Reorder objectives
        - View history, analytics, and discussion
        - Reorder
        - Notifications
        - Consensus editing
        - Tips
- **Information**
    - _Learners_
        - See information in my language
        - Flag problematic information
        - See information well isolated from interface or other screen objects
        - Default to seeing the best information possible
        - Able to skip, ask for a different presentation
        - Able to recall presentation or summary
        - Able to see related learning objective(s)
        - Able to discuss presentation with other learners and mentors
        - Observe progress at any point in time
    - _Contributors_
        - Select related objective
        - View history, analytics, and discussion
        - Consensus editing
        - Upload in a variety of formats
        - Add interjected questions
        - Add interactive or simulated
        - Learning science tips
- **Practice**
    - _Learners_
        - Receive practice in my language
        - Flag problematic questions
        - Questions adjust to my prior knowledge and current skill level
        - Receive feedback on answers
        - Allowed multiple attempts where suitable
        - See relevant learning objective(s)
        - Discuss question with other learners and mentors
        - Observe progress at any point in time
        - Able to skip question or ask for a different question
        - Use practice sets for longer questions
        - Review prompts or summaries for prior knowledge
    - _Contributors_
        - Select related objective
        - View history, analytics, and discussion
        - Consensus editing
        - Feedback entering
        - Format variety
        - Number of tries
        - Synchronous or asynchronous
        - Learning science tips
- **Application**
    - _Learners_
        - Able to choose from a variety of projects
            - Understand time scope
            - See reviews of other learners
            - Understand technical requirements
        - Able to ask for a different project
        - Assessed of understanding of project proposal
        - View rubric of how the project will be assess
        - Asked to evaluate project, plan it out
        - Able to discuss project with other learners and with mentors
        - Submit work on project for review
        - Review others works
        - Asynchronous with learning environment:
            - Some projects can't be assess immediately
            - Receive notification when assessment is complete
            - Components and integration progress must reflect project state
        - Receive quality reviews from other learners
        - Invited to reflect on experience of project work
    - _Contributors_
        - View history, analytics, and discussion
        - Consensus editing
        - Format, feedback, tries, synchronous/asynchronous
        - Step-by-step process for learner metacognitive support
-  **Relationships, Integration, Module**
    - _Learners_
        - Easily find a suitable module for learning objective
            - See reviews
            - See estimated length for completion (in hours)
        - See organizational schema at any point in time
        - See progress in organizational schema
        - Receive and implement diagnostic assessment
        - Receive terminal assessment and project to close the module
        - Regularly review material to retain in memory
        - Encourage and reminded to work on module
        - Integrations should not add new material; but simply integrate prior material
    - _Contributors_
        - View history, analytics, and discussion
        - Consensus editing
        - Specify prerequisites, no closed loops
        - Merge and split operations
        - Notifications
