---
layout: post
title: 'Choosing an Open-Source License'
description: 'I have to start this article by saying I’m not a lawyer, and nothing in this article is legal advice. If you are looking for a legal recommendation, ask an attorney. When I started Sagefy back in…'
date: '2016-10-16T18:18:46.879Z'
---

_How I chose the Apache 2 license for Sagefy._

I have to start this article by saying **I’m not a lawyer**, and nothing in this article is legal advice. If you are looking for a legal recommendation, ask an attorney.

## Why Sagefy is open source

When I started [**Sagefy**](https://sagefy.org) back in April of 2013, I wanted to build a system where [**anyone can learn anything**]({% post_url 2016-09-14-why-i-m-building-sagefy %}). Where learning is accessible to every learner. Where the experience is completely _adapted_ to the learner’s goals and prior knowledge. Accelerating human learning is the best investment we can make.

I knew I wanted to go **open source**. Open source software has permanence, collaborative environment, and freedom from the profit motive. My passion for accelerating human learning needs the open source perspective. _Financial incentives overwhelm education._ The open source mindset and my objectives fit perfectly. I’m a true believer in the [power of open source software](http://www.catb.org/esr/writings/cathedral-bazaar/).

![https://choosealicense.com](/images/choose-1.png)

## The problem with picking a license

In short, the first decision is _if you want to develop your project in_ **_open source_**. For Sagefy, I wanted to go in the open source direction.

Software engineers often default to create their personal projects on [Github](https://github.com/) in public. Yet, tech companies almost always default to building proprietary systems. It’s a strange conflict. The reason for the conflict is between the values of entrepreneurship and the values of the open web.

Once you’ve decided to go open source, the next decision is: **choosing a license**. For Sagefy, this decision was a more difficult process. The Open Source Initiative _lists_ [_78 acceptable open source licenses_](https://opensource.org/licenses/alphabetical) _currently_. And that’s only for the code! For content, there’s even more options. Each of these licenses look similar on the surface, but the differences are astronomical. Different values, different concerns, different strategies, different implications, different compatibility.

_I first chose AGPL3 for Sagefy._ I didn’t know much about the different licenses. I knew I was creating a web service, and AGPL3 covered this use case. I popped the license in, and didn’t think much about the issue for a few months.

## Most popular licenses

The first consideration in choosing a license is to **go with a popular license**. With a popular license, people know what the license means. People know what the restrictions are, and know how to interact with the project. With less common licenses, its more work for contributors to understand the rules. An uncommon license may deter contributors and adoption. Furthermore, popular licenses are popular for good reason: _the community vetted them_.

So which licenses are the most popular? It’s difficult to say because there’s so many different ways to measure. GitHub is about as neutral and as large as we can get. According to their [2015 blog post,](https://github.com/blog/1964-open-source-license-usage-on-github-com) the **MIT license** is by far the front runner with _44% of all licenses_. That’s not surprising to anyone in the open source world. The MIT license is permissive and compatible.

The next two most common are **GPL2** and **Apache 2**. Apache 2 is popular with corporations. Corporations see Apache 2 as a more formal version of the compatible MIT license. GPL2 has a history with Linux. Other popular licenses are **GPL3** and **BSD 3-clause**. _Unlicense_, _BSD 2-clause_, _LGPL3_, and _AGPL3_ round out the top. Each of those last four are about 1–2% of all licenses each.

## Reviewing license options, conflicting values, impacts

I further researched about setting up an open-source project. I realized I knew little about the differences between the licenses. So here’s my non-lawyer take on them. Please note I am **NOT A LAWYER**. _And this is not legal advice_. If you have questions, you should talk with an intellectual property attorney.

### The permissive licenses: MIT, Apache 2, BSD 2-clause, BSD 3-clause, and Unlicense

If I want a super permissive license or have no idea what I want, **I pick MIT**. If I am concerned about patents, contributor agreements, or trademarks, **I choose Apache 2**. Be aware if you pick Apache 2, other open source projects under GPL2 may be reluctant to use your project.

The [**MIT license**](http://choosealicense.com/licenses/mit/) is short. The MIT license appeals to the ideal of minimalism. The MIT license pretty much just says:

- You can _do almost anything_ you want with this code.
- You have to _include the license_ if you redistribute this code.
- The author waives any warranties. _You’re on your own_.

The MIT license is by far the most common for a reason: it’s _simple_ and _easy to understand_.

[**Apache 2**](http://choosealicense.com/licenses/apache-2.0/) is often used for large projects and corporate backed projects. Despite being many times the length of the MIT license, the Apache license is similar. The length includes definitions of legal terms to avoid ambiguities. Apache 2 adds the following to the scope of the MIT license:

- The authors are allowing you to use _patents_ related to the code.
- If you redistribute the code, you need to _state what changes_ you’ve made.
- _Contributor works_ in the project are under the same license.
- You can’t use the authors’ _trademarks_ as your own.

Unfortunately patents are a major problem in the software world currently. That’s the main draw of the Apache 2 license. Protecting trademarks are within most corporate interests. And it’s not clear if open source projects need [Contributor License Agreements](https://en.wikipedia.org/wiki/Contributor_License_Agreement). Apache 2 addresses these concerns.

There’s an unfortunate dark side to the Apache 2 license. _GPL2 licensed projects may not be able to consume your project_. The GPL**_3_** licenses are all okay with consuming Apache 2 code. There’s disagreement between different groups about if Apache 2 and GPL**_2_** are compatible. I don’t agree there’s a compatibility issue. The [position of the Free Software Foundation](https://www.gnu.org/licenses/license-list.html#apache2) is there is a compatibility issue.

The [**BSD 2-clause**](https://opensource.org/licenses/BSD-2-Clause) is like the MIT license. As a non-lawyer, I can’t tell the difference, if there is any. The [**BSD 3-clause**](https://opensource.org/licenses/BSD-3-Clause) adds a third clause. If the original authors don’t endorse your work, you can’t pretend the original authors do. Granted, in real life, I don’t think you can’t make that claim regardless. The 2-clause is actually the younger form. I don’t see much reason to use the 3-clause over the 2-clause. I can’t say I would ever use either BSD license over the MIT license.

[**Unlicense**](http://choosealicense.com/licenses/unlicense/), which despite its name is a license and is like the MIT license as well. To the scope of the MIT license, the Unlicense includes the following:

- A _public domain_ release statement.
- Nothing says you _need_ to include the original license.

I can’t imagine there’s much of a practical difference between MIT and Unlicense. _Again, speaking as not-a-lawyer_.

### The copyleft licenses: GPL2, GPL3, LGPL3, AGPL3

The split here comes down to values. If you want anyone to use your software — a person, an organization, a business, whatever — then permissive licenses are the way to go. But, if you want derivatives _to stay completely in the realm of open source_, **GPL** may be the right way to go for you. If you choose a copyleft license, many companies will be _reluctant_ to use your software. _The essence of a copyleft license is derivative works must use the same license._

[**GPL2**](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html) is the license of Linux. The bullet points:

- You can _do almost anything_ you want with this code.
- You must _include the original license_ in forks.
- Copyleft: Derivatives must be _under the same license_.
- No warranties. _You’re on your own_.

At a glance, just from these items the main difference from MIT is the _copyleft part_. The full license does get a bit more technical about specific legal situations.

The [first author of Linux feels](http://www.informationweek.com/the-torvalds-transcript-why-i-absolutely-love-gpl-version-2/d/d-id/1053128?) this license is the best for his work. His reason is something like: “there should only be _one true_ open source license and not a variety of them.” Many large projects use GPL2 instead of GPL3 for this reason.

I agree the decision can be _difficult to figure out which license_ is the right one for a given project. But on further examination, different teams value different things. And that’s okay.

The [**GPL3**](http://choosealicense.com/licenses/gpl-3.0/) reads like the GPL2 license. GPL3 addresses patents, [digital rights management,](https://en.wikipedia.org/wiki/Digital_rights_management) compatibility with other licenses, and license violations. GPL3 code is able to consume Apache 2 projects. If you want alignment with other projects already doing so, use GPL2. Otherwise, I can’t say I find a compelling reason to use GPL2 over GPL3.

The [**LGPL3**](http://choosealicense.com/licenses/lgpl-3.0/) softens some of the copyleft of the plain GPL3. You can “_link_” to the project without the copyleft coming into play. We can debate what linking means, but you are giving an “out” to the copyleft provision. The [**AGPL3**](http://choosealicense.com/licenses/agpl-3.0/) tightens those restrictions: using the project “_over a network_” triggers copyleft.

GitHub created the website [http://choosealicense.com/](http://choosealicense.com/). This website puts the top 3 licenses as the MIT License, Apache 2, and GPL3. That’s a good representation.

This article doesn’t describe all 78 open source licenses. But _maybe_ one of the other licenses is a better fit for your project. That’s up to you.

## My Criteria

I would start out a new project with the following criteria:

- Do I want _copyleft_?
- — …and do I care about over _network_ use? **AGPL3**.
- — …do I want alignment with other projects? **GPL2**.
- — _Else_, **GPL3**.
- Else…
- —Do I worry about patents, contributor license agreements, or protecting my brand? Am I not concerned about GPL2 projects? **Apache 2**.
- _— Else_, **MIT**.

These would be my criteria. I’m not making a recommendation here. If you need a recommendation, then you need to speak with an attorney.

## Chosen license: Apache 2.0

I chose to change Sagefy from AGPL3 to Apache 2.0. I was the only contributor up to that point. I had no concern of getting other contributors to agree to the license change.

**Do you want copyleft?** That decision makes the biggest difference. I want anyone who wants to use Sagefy to be able to do so. I want schools, other organizations, and corporations to set up their own instances. The copyleft provision makes people nervous. I’m amused no one second guesses using _Linux_ or _Wordpress — they’re both GPL2._ But for other projects, people worry.

Getting more people to use your project means you’ll get contributions more quickly. You won’t get the same percentage out in the public. 100% for copyleft, less than 100% for permissive. But do you want 100% of a smaller number, or less than 100% of a larger number? Different projects answer differently.

That decision would have led me to MIT by default. For Sagefy, there’s _benefit_ to gaining the extra provisions from Apache 2.0. I have no real concern about GPL2 licensed software consuming Sagefy. _Not_ that I would have a problem with a GPL2 project using Sagefy, just I don’t see that scenario as a likely use case.

## The future

Sagefy will most likely stay with Apache 2. If there were to make any change at this point, the most likely would be to the MIT license. I don’t know of any lawsuits with the MIT license specific to patents, contributor license agreements, or trademarks. Perhaps Apache 2 isn’t necessary. _Yet, as the questions remain open, that’s the environment we’re in_.

**The law constantly changes.** Both in the body of the law and in the interpretation of the law. Because the law changes, so too will open source licenses. I wish we could have the ultimate, one single true open source license. The **MIT license** is the closest thing we have currently. _But the law will change, and new licenses will adapt to those requirements._

When you’re first making an open source project, choosing a license can be _overwhelming_. Decide if copyleft is the right decision for your project. If you do want _copyleft_, you need to decide how strong you want the copyleft. If you don’t want copyleft, you can choose between: a _simple_ permissive license, or an _aware_ permissive license.

_Any license you choose_, open source software is changing the world faster than anything else. **Come on in!**

If you’d like to know more about Sagefy, [visit today](https://sagefy.org).
