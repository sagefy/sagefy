---
title: Data Structure
layout: default
---

This document covers the overall architecture of Sagefy's data storage. This data structure allows Sagefy to be both open-content as well as highly adaptive and flexible while maintaining practicality.

_TODO: Visual demonstration_

See also [Data Structures and Users](/data_structures_and_users).

Cards
-----

Cards are the smallest entity in the Sagefy data structure system. A card represents a single learner activity.

A card could present information, ask the learner to answer a question, collaborate with a small group to tackle a challenge, or create other cards.

### Card Kinds

Some kinds may include:

- An informational presentation
    - A reading passage of text, with images and diagrams
    - A plain slideshow
    - A slideshow with audio narration
    - A radio show
    - A video
    - A timeline
- A practice question
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
- An application of knowledge
    - Individual, collaborative, or team.
    - Any of the following
        - **Accept**: Provide the learner with a description of the task.
        - **Assess**: Assess the learner's understanding of the task.
        - **Analyze**: Analyze the problem and the context. Brainstorm strategies and pros and cons.
        - **Plan**: Ask the learner to evaluate the task, break it into parts, and form a plan.
        - **Act**: Have learner implement their plan.
        - **Peer Review**: Have the learner evaluate other's work on the same task.
        - **Self Review**: Invite learner to review evaluations of the learner's work.
        - **Reflect**: Invite learner to reflection on project experience.
    - Rubrics system: provide a systematic means of evaluation.

### Card Categories

Some categories may include:

- Worked examples
- Application examples
- Motivational examples
- Comparisons

### Card Requirements

- A card must relate to a learning objective within a unit.

### Card Guidelines

- Cards can form relationships with each other.
    - _TODO: Kinds of relationships?_
    - _TODO: Projects as card series..._
- Cards can vary in length, but generally should be shorter than 10 minutes.

Units
-----

A unit is the medium size in the Sagefy data structure system. A unit represents a unit of learning activity.

An example of a unit is a small learning lesson, which may contain about five to eight minutes of information and 30-60 minutes of practice to gain proficiency.

A unit may also represent an **integration** of other units. In this case, a prerequisite tree would automatically form.

A unit contains multiple cards.

A unit is defined by a single goal (objective). See [Bloom's Taxonomy](http://en.wikipedia.org/wiki/Bloom's_taxonomy).

### Unit Categories

- Unit categories may include Bloom's Taxonomy

### Unit Requirements

- Units are language specific.
- Units must be the same language as the set.
- Must describe a specific learning objective.
- Unit prerequisites cannot form a cycle.

### Unit Guidelines

- The unit goal should be described to the learner at the beginning.
- The current goal must be available to the learner at all times.
- Can establish prerequisite units. (Keep it very specific.)

Sets
----

A set is a collection of units and other sets. A set describes a course of units that meets a larger objective, such as knowing the basics of American Sign Language or Japanese Art History.

A graph is automatically formed based on the units and sets specified. Any chaining units or sets or necessary learner prerequisites would be automatically included.

### Set Categories

Set categories would need to be community-defined.

### Set Requirements

- A set must contain at least one unit or set.

### Set Guidelines

- Most sets should be described as either a collection of "base" units or a collection of sets.
