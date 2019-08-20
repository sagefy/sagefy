---
layout: post
title: 'How to build an adaptive learning system'
description: 'The four elements of adaptive learning systems.'
image: /images/adaptive-1.jpg
published: false
---

In this article, I'll go over what adaptive learning systems are. I cover some background on why adaptive learning systems have the structure they do. I'll introduce a few adaptive learning systems. Then, I talk about the four elements. And how you can architect an adaptive learning system. We'll wrap up with evaluating the pros and cons of adaptive learning.

## What is an adaptive learning system?

An adaptive learning system is software where algorithms optimize the content to adjust for the learner's goals and current state of knowledge.

In a traditional e-learning course, you will linearly follow the path an instructor creates. You watch videos, read articles, take quizzes, and practice interactive modules in a predetermined ordered. An adaptive learning system will contain the same types of materials. But the order will change for each learner. The system decides which content to show the learner based on two things:

- If the learner's **goal** is only a subset of the overall content, the system can limit the content.
- The **prior knowledge** also comes into play. If the system determines the current path is too easy, the system can accelerate to more challenging material. If the system finds out the current path is too difficult, the system may intervene and review prerequisite content, reduce the challenge, and slow down the pace.

Some related topics include intelligent tutors, adaptive testing, psychometrics, personalized learning, and smart teaching. Many of these topics share algorithms and structures with adaptive learning systems.

![](/images/adaptive-2.jpg)

## Knowledge is a graph: neuroscience

I'm going to start with a little background. This will create context for why adaptive learning systems have the four elements below. The point for all of this is _knowledge is a graph_.

The human brain has 86 billion neurons. Every neuron has dendrites, a soma, and an axon.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Blausen_0657_MultipolarNeuron.png/1200px-Blausen_0657_MultipolarNeuron.png)

- The **dendrites** are the _input_. The edges of the dendrites receive neurotransmitters from the synapse. The synapse is a gap between two neurons.
- The **soma** is the _throughput_. The soma -- which contains the cell nucleus -- routes the input from the dendrites.
- The **axon** is the _output_. The axon transmits an action potential -- an electrical signal -- to the axon terminals. A myelin sheath covers the axon to protect the signal. The axon terminals release neurotranmitters into the synapse.

As your brain receives and processes information, that information will correspond with a neural pathway in your brain. Your brain with _myelinate_ that pathway -- strengthen the myelin around the axon to support electrical signals. Because of the strengthened myelin, this path will be more likely to fire in the future. In other words, you learn.

Even in the smallest scale, our brain is a massive graph of connected neurons. We learn and optimize by making some paths more likely to connect than other paths.

## Knowledge is a graph: learning science

The strongest predictor of how we perform in a learning environment is our prior knowledge -- what we already know before we start the learning experience. A notable psychology paper -- 1999 Dochy, Segers, and Buehl -- found prior knowledge accounts for about 81% of the learning outcome differences between different learners. Reviewing prior knowledge before showing new information can have a dramatic impact on learning outcomes. And connecting new knowledge to prior knowledge while teaching can have a big impact too. (See [Eight Ideas]({% post_url 2018-07-09-eight-big-ideas-of-learning %}) for sources.)

Perhaps the most famous psychology paper is 1956 "The Magical Number Seven, Plus or Minus Two: Some Limits on Our Capacity for Processing Information" by George Miller. The paper suggests that humans have a limited working memory. Miller found for simple numbers, a human could work with about seven items at once. Later researchers found for more complex information, that limit is closer to four.

Some psychologists suggest of these "four slots", for us to learn, at least one or two must be prior knowledge. How much prior knowledge we can "load up" into one of the four slots depends on the strength of the connections in the graph. When we have both prior knowledge and new knowledge in our working memory, we associate the information and strengthen the connection between the two. Trying to learn new information without connecting to prior knowledge limits the strength of the memory.

In short, we learn by connecting prior knowledge to new information. And those connections form a large, endless graph of knowledge.

## A few important adaptive learning systems

This section is more context, but optional. I'm not writing an thorough article about the history of these systems, but here's some bullets:

- One of the earliest implementations was the [Skinner teaching machine](https://en.wikipedia.org/wiki/Teaching_machine).
- During the 1960s and 1970s, there were several attempts at computerized instructional systems. Costs and slower machines limited the success of these systems.
- During the late 70s and early 80s, [Item Response Theory](https://en.wikipedia.org/wiki/Item_response_theory) enabled test makers to start work on computerized adaptive testing.
- An early and influential computerized system was the Lisp tutor, also known as LISPITS (1983) at Carnegie Mellon University.
- [SuperMemo](https://en.wikipedia.org/wiki/SuperMemo), released in 1985, incorporated spaced learning into a computerized system.
- Also in 1985 came paper for [Knowledge Spaces](https://en.wikipedia.org/wiki/Knowledge_space), which forms the foundations of one of the four elements.
- [ALEKS Math tutor](https://en.wikipedia.org/wiki/ALEKS) came out in 1994, heavily promoting its use of knowledge spaces.
- In 1995, Corbett and Anderson published "Knowledge tracing", forming the foundation for [Bayesian knowledge tracing](https://en.wikipedia.org/wiki/Bayesian_Knowledge_Tracing) models.
- Some important software includes [AutoTutor](https://en.wikipedia.org/wiki/AutoTutor), [ACT-R](https://en.wikipedia.org/wiki/ACT-R), and [Cognitive Tutor Authoring Tools](http://ctat.pact.cs.cmu.edu/).
- [Knewton](https://en.wikipedia.org/wiki/Knewton) is an example of contemporary adaptive learning systems. Kaplan and Pearson both use Knewton to provide adaptive learning experiences.

## The four elements

Nearly all adaptive learning systems today have these four elements. The terms change slightly and so do their scope. But you will almost always find all four elements.

These elements are:

- The **expert** -- a graphical model of the "ideal" state, of everything the person could learn using this system.
- The **learner** -- a model of the learner's current state, which shows how likely the learner is to know each of the nodes in the expert graph.
- The **tutor** -- the algorithms that determines what content to show and when. The expert model and the learner model inform the tutor. The tutor seeks to optimize content for relevance, challenge, and efficiency.
- The **interface** -- which is how to display the learning experience to the learner. In many adaptive learning experience, the interface changes based on the learner model and the tutor's goals.

Let's go into each element.

![](/images/adaptive-3.jpg)

### The expert — the big graph of everything

TBD

![](/images/adaptive-4.jpg)

### The learner — where you are versus where you want to be

TBD

![](/images/adaptive-5.jpg)

### The tutor — what to show when

TBD

![](/images/adaptive-6.jpg)

### The interface — how to show it

TBD

![](/images/adaptive-7.jpg)

## How do we know if adaptive learning is any good?

As these systems come from academia, we have a significant amount of data and history with each system.

An established finding in educational research is one-on-one human-to-human tutoring has the strongest learning outcomes. So far, no computerized adaptive learning system has outperformed human one-on-one tutoring.

Researchers have investigated classroom learning alone, computerized adaptive learning alone, as well as combined classroom and adaptive learning. A [2016 paper "Effectiveness of Intelligent Tutoring Systems"](https://www.researchgate.net/publication/277636218_Effectiveness_of_Intelligent_Tutoring_Systems_A_Meta-Analytic_Review) provides a meta analysis of these studies. Adaptive learning systems usually outperform traditional classroom learning. Combined with classroom learning, adaptive learning systems create a positive effect, but there are some limitations.

Adaptive systems do particularly well with instant feedback and ensuring skill mastery. However, investigators note some areas for improvement:

- The cost of developing content for these systems is high.
- These systems often can't contextualize learning the way a human can.
- Adaptive learning systems can feel more challenging, which can reduce learner motivation.

## Wrap up

Welp, I've nerded out now. I've covered what adaptive learning systems are. I've provided some context for the design of these systems. A touch of history. I've covered the four major elements: the expert, the learner, the tutor, and the interface. Hopefully it wasn't too technical.

Obligatory end-of-article call-to-action: [Check out Sagefy](https://sagefy.org), the open-content adaptive learning system I'm working on.
