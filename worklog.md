Sagefy Work Log
===============

2015 Jan 12
-----------

**Weekly Goal**: Complete unit tests: #152, #153, #154, #155, #156, #158, #159.

Moving to use Bayesian updates of guess and slip with PMF.

2015 Jan 11
-----------

Explicitly listing requirements for primary learning system. Scaffolded routes and models for learners.

2015 Jan 10
-----------

Working on PMF version of guess and slip updates. Results so far are somewhat worse than the weighted mean model.

2015 Jan 09
----------

Bayesian update of guess and slip optimized to 0 or 1... so I believe a PMF would need to happen instead. Mocking up a PMF class to use to try out Bayesian guess and slip updates.

2015 Jan 08
-----------

Discovered Bayesian update formulas for guess and slip. Testing soon...

2015 Jan 07
-----------

Scaffolding model unit tests.

2015 Jan 06
-----------

Update models to new model module.

2015 Jan 05
-----------

**Weekly Goal**: Complete unit tests: 152, 153, 154, 155, 156, 158, 159. Begin code for discuss API.

Using scaled formula for unit quality and unit difficulty, completing the aggregates.

2015 Jan 04
-----------

Updated sequencer documentation with formulas.

2015 Jan 03
-----------

Found acceptable model for `belief`.

2015 Jan 02
-----------

Found acceptable model for `transit` updates. Clean up some Github tasks.

2015 Jan 01
-----------

Worked on learner planning: models and endpoints.

2014 Dec 31
-----------

Updated year to 2015. Moved contributing notes to [CONTRIBUTING.md](https://github.com/blog/1184-contributing-guidelines). Finished first draft of learner wireframes.

2014 Dec 30
-----------

Accepted weighted mean variant of guess and slip updates... for now. Odd that slip prefers learned^3 rather than learned^2 (weight * chance). Beginning work on transit.

2014 Dec 29
-----------

**Weekly Goal**: Write out major use cases. Finish first draft of learner wireframes. Ensure base functions work as expected in simulation. Work on formula for guess and slip updates.

Working on 'weighted mean' style of updates for guess and slip. Wrote major use cases.

2014 Dec 28
-----------

Started work log. Started weekly goals. Outlined expectations for guess and slip updates.

Initial Entry
-------------

I'm starting a work log for Sagefy, with the hopes that it will motivate me and provide way to visualize my progress towards the first MVP. In the future updates will be a short description of what I did for the day, even if the activities don't directly involve pushing code. The grammar and spelling will not always be perfect here.

So far, here's the big ticket items I've completed:

**Vision**. Years ago, I asked myself the question, if there was one thing I could build to make an impact, what would it be? My [blog post on why I'm building Sagefy](https://heiskr.com/2014/09/21/why-sagefy/) lists out how I came to working on this project. It took me a long time just to articulate the basic phrase, "open-content adaptive learning platform."

**Research**. I've read some great books on learning science and in particular adaptive learning systems. I've taken a few online courses and read my share of academic papers. Some of the books that influence me the most are [How Learning Works](http://www.amazon.com/How-Learning-Works-Research-Based-Principles/dp/0470484101), [Building Expertise](https://www.amazon.com/dp/0787988448), and [e-Learning and the Science of Instruction](http://www.amazon.com/Learning-Science-Instruction-Guidelines-Multimedia/dp/0470874309/ref=dp_ob_title_bk). I've taken ideas from the [spaced repetition camp](http://www.supermemo.com/english/contents.htm). Perhaps the course that has influenced me the most was [Big Data in Education](https://class.coursera.org/bigdata-edu-001) by Ryan Baker. Much of the UI design comes from my own experience from UX research and several books in that area, such as [Elements of User Experience](http://www.amazon.com/The-Elements-User-Experience-User-Centered/dp/0735712026). I've taken an insane amount of notes, and boiled down everything to [7 major principles](https://docs.sagefy.org/ideas) that seem to repeat over and over again. Research is a continuing effort.

**Definition**. At the same time, I've been defining, from the big picture, how I envision Sagefy would be structured. I've tried to keep it very flexible and simple, allowing for room for growth in the future. My progress there can be found in the [docs](https://docs.sagefy.org/).

**Technical Stack**. I chose my [technical stack](https://docs.sagefy.org/f_technology/stack) and began setting up the infrastructure and [technical direction](https://docs.sagefy.org/f_technology/contribution).

**User Accounts**. I've created the basic abilities for users to create accounts, login, logout, change their password, and read notifications.

**Planning**. I've started planning on [how people will contribute](https://docs.sagefy.org/f_planning/user_accounts) and how the [learning process](https://docs.sagefy.org/f_planning/contributors_mvp) will work.

Other activities, from the git log:

- Picked the name
- Decided on AGPL
- Created the logo
- Created a style guide / component library
- Setup Travis CI
- Setup local vagrant development
- Drafted temporary TOS
- Setup docs site with Github Pages and Cloudflare
- Setup UI build system
- Setup API server config
- Wrote an ODM
- Unit testing for both the UI and API
- ...a million other little tasks

**Current Activities**. I'm prototyping the learning system math and continuing planning, definition around contribution and learning, and writing unit tests for those features.
