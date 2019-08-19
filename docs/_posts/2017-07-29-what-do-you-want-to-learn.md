---
layout: post
title: 'What do you want to learn?'
description: 'Why and how I built a community page for anyone to share what they want to learn.'
date: '2017-07-29T03:05:00.517Z'
image: /images/what-1.png
---

**The Suggest page on** [**Sagefy**](https://sagefy.org/) **allows you to suggest new free online learning subjects.** And you can up-vote subjects that interest you. And you _don’t_ need to sign up for an account! Why use the Suggest page? Maybe you can’t find something you’re looking for. Maybe you’re thinking about building something but want to see what the interest level is first. Or you’re looking for a different approach to something that already exists.

In this article, I’m going to go into the background about the Suggest page.

## What is Sagefy

**Sagefy is an open-content adaptive learning system.** _Open-content_ means anyone can create and update learning content, like Wikipedia. _Adaptive learning_ means the content changes based on the learner’s goal and their prior knowledge. The combination means anyone can learn almost anything, regardless of their prior knowledge. To learn more about Sagefy, check out [this in-depth article]({% post_url 2016-09-14-why-i-m-building-sagefy %}).

## How the Suggest page idea came about

So far, Sagefy is at [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) quality code-wise and I have a full electronic music intro course built out in Sagefy.

I’d like to build more **content** along with collaborators. I also want to continue to **improve functionality**. To support these efforts, Sagefy is going to need a _revenue stream_. Even if Sagefy does become non-profit, donations and grants are tough to come by. Finding a revenue model is a priority.

I’ve committed to myself to **not** put up [paywalls to access learning](https://medium.freecodecamp.org/massive-open-online-courses-started-out-completely-free-but-where-are-they-now-1dd1020f59). I’m looking for a revenue model that would also encourage _content creation_ as well as _learning_. Finally, more than one revenue resources is better, to reduce risk.

I’ve brainstormed about a dozen ideas that met this criteria, but I have **no idea** which ones might actually work. Everyone thinks they know what product-market fit is going to be in advance, but no one does in practice. Product-market fit always seems obvious in hindsight. _When you’re in the driver’s seat, the road is much more foggy._ I’m not investing a ton of time in predicting and planning the perfect solution and build it all the way. I’m trying little experiments. Get out the [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) to see if the idea will work and see what the response is.

I picked the Suggest page experiment first because its had some of the lowest technical requirements of the ideas I’ve had so far. And the Suggest page _meets the criteria_ I mentioned above — doesn’t block access to learning, encourages content creation, and encourages learning.

The Suggest page may not even seem like a potential revenue source. Right now, _it isn’t_ creating revenue. If the Suggest page succeeds, the idea is to allow anyone to make a **bid** on the suggested courses, and let others **pledge** funds towards the bid. If the amount reaches the bid’s minimum, the content gets funded. Sagefy would take some small percentage of the funding to support Sagefy itself. I don’t need the bids or pledges to see if the idea will work. I need to know if people are _willing_ to suggest and up-vote ideas for free online learning content _in the first place_. There’s many sites that already do crowdfunding of course, but I’m not aware of any strictly related to funding free online learning content. And of course, the Suggest page is one idea.

## How I built the page quickly

Because the Suggest page is an experiment, I did not build the page into the main Sagefy ecosystem. The Suggest page exists as its own Nginx route. In fact, **all the code is in** [**one file**](https://github.com/heiskr/sagefy/blob/master/suggest/index.py). There’s not even a framework; the only library is for the database. And of course there’s _no_ _automated tests_. I also did not write any JavaScript for the page. The whole thing is **plain old HTML** and barely any CSS. It’s about as bare bones as possible. You can build a surprising amount with this sort of setup, and get the experiment done very quickly.

Not doing things the “right” or “modern” way, I built the whole page in _less than 4 hours total_. I may have been able to find something out there that produces similar functionality. But I would have spent as much time searching as I did coding. With experiments going forward, I may or may not end up writing code for them… depends on the idea and what’s already out there.

If I built this page the “correct” way , this experiment would have taken 20 or more hours. Tests, frameworks, scaling, splitting off the API from the UI, and so on. _Coding things the “old” way means I can do more experiments with more frequency._ Its sort of fun to relive the glory days when feature expectations on the web were so much lower. If the Suggest page is successful, I’d want to update the approach to be more more feature-capable than plain old HTML.

## The process for creating new experiments like this

I still have several more ideas I’d like to try out to see if I can find a revenue model for Sagefy. If you’re going through this too, here’s what the **step-by-step process** looks like:

1.  Create, review, and update the **criteria** for revenue models.
2.  **Brainstorm ideas** that would fit the criteria. Think about the user’s _circumstances_ and what could help solve the _problems_ they have. Also, try looking an _existing_ models.
3.  **Pick the idea** you think will meet the criteria with the least amount of _effort_ to try the idea. Don’t be afraid of using Google Forms or other existing services to get the idea out as quickly as possible. _It’s an experiment, not a commitment._
4.  **Build** the experiment quickly and cheaply. _Verify the idea_, not necessarily actually generating revenue right away. Avoid making people do anything other than the task at hand, such as signing up for an account. Anything more than a few seconds worth of effort will deter people.
5.  Don’t show a blank page. Add some **real content** before you start to promote the experiment.
6.  **Promote** the experiment. No one’s going to show up because you built it. Go to sites where the audience is _already browsing_, and share a link.

## Going forward

So far the Suggest page got a bit of initial traffic, but the interest has waned since then. I’d guess about 100 people have either suggested an idea or up-voted one. I’m not ready to count this as an unsuccessful quite yet. With some promotion the Suggest page could have potential. I don’t have a ‘exit plan’ as there’s no costs involved, so the Suggest page is going to be around for the foreseeable future.

I’m going to try some more experiments too. All while also continuing to improve Sagefy’s learning and contributing experiences. _So… keep your eyes open for improvements and more experiments too!_

## Try out the Suggest page

If you’ve made this far in the article, congrats! That, and **you should try out the Suggest page.** No need to sign up for an account. You can up-vote existing ideas and add your own. _And let me know your feedback too!_

If you’d like to know more about Sagefy, [visit today](https://sagefy.org).
