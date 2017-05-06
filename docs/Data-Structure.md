---
layout: docs
title: Data Structure
---

This document covers the overall architecture of Sagefy's data structure. This data structure allows Sagefy to be open-content, flexible, and practical.

![Data Structure Example: Statistics](https://docs.google.com/drawings/d/1idC1i8udNsD5C1yj1K7qKp6cwSkyhwjLXzG-xsXG6gE/pub?w=735&amp;h=280)

There are three types of entities in Sagefy: cards, units, and subjects.

**Card**. A card is a single learning activity. Examples include a short video, a multiple choice question, or a single math problem. An example question would be, "What is the median of 5, 7, and 10?" Cards are the smallest entity in the Sagefy data structure. A card always belongs to a single unit.

**Unit**. A unit is a single learning goal. A unit is similar to a short, hour-long lesson. An example would be, "describe the differences between mean, median, and mode." A unit is the medium size entity in the Sagefy data structure. A single unit has many cards. A unit can require other units before it. A unit belongs to many subjects.

**Subject**. A subject is a collection of units and other subjects. Subjects are like classes or courses, anything from like a short workshop to an entire degree program. Examples could be, "measures of central tendency", "descriptive statistics", or "first statistics course". A subject is the large size in the Sagefy system. A subject contains many units and other subjects.

Also see [Data Structure: Requirements and Guidelines](Data-Structure-Requirements-and-Guidelines).

Also see [YouTube Video](https://www.youtube.com/watch?v=HVwfwTOdnOE).
