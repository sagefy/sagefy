---
layout: docs
title: Cards & Subjects
---

_There are two types of entities in Sagefy: cards and subjects._

- A **card** is a single learning activity.

  > Examples: a 3-minute video or a multiple choice question.

- A **subject** is a collection of cards and other subjects.

  > Like a course, but at any scale. Such as “Measures of Central
  > Tendency”, “Intro to Statistics”, or even a complete statistics program.

![Data Structure Example: Statistics](https://docs.google.com/drawings/d/1idC1i8udNsD5C1yj1K7qKp6cwSkyhwjLXzG-xsXG6gE/pub?w=735&h=280)

For more details and examples, [check out this 3-minute overview video](https://youtu.be/gFn4Q9tx7Qs).

## Card Requirements

- A card must have a name.
- A card must belong to a single subject.
- A card must belong to a single subject of the same language.
- ~~A card can have before and after cards (prerequisites). These cannot form a cycle.~~
- Each card kind has its own requirements.
- For more card kinds, see [Card Kinds](Card-Kinds).

## Subject Requirements

- A subject must have a name.
- A subject must have a written goal.
- A subject's goal can be anywhere from narrow to broad.
- Subjects may only contain cards and subjects of the same language.
- A subject may have a single parent.
- A subject may have many children
- A subject can have before and after subjects (prerequisites). These cannot form a cycle.

What's next? [Continue to "Want to Help?"](/Want-to-Help).
