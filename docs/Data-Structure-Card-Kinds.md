---
layout: docs
title: Data Structure> Card Kinds
---

_This documents kinds of cards that may appear in the Sagefy system._

Anywhere that lists "Markdown" as available may embed images, math, video, audio, interactive...

## Unscored Card Kinds

Unscored cards do not have require a learner response.

### Video Card

An embedded video from a popular video hosting site.

- site: youtube, vimeo, ...
- video_id

### Page Card

A textual-based document.

- body: Content of the page. (Markdown)

### Audio Card

An embedded audio from a popular audio hosting site.

- site: soundcloud, ...
- audio_id

### Slideshow Card

An embedded slideshow from a popular slideshow hosting site.

- site: slideshare, ...
- slideshow_id

### Unscored Embed Card

An embedded unscored learning object.

- url

## Scored Card Kinds

Scored cards require a response from the learner and are graded immediately and automatically.

### Choice Card

A choice card, also known as multiple choice or multiple answer, is as expected. It also can represent a true or false type of question.

- body: Question. (Markdown)
- options: List of available options
  - value: Text of the option (Markdown)
  - correct: At least one option must be marked as correct. If only one option is marked as correct, it will be a single-choice (radio); but if more than one option is marked as correct, it will be a multiple-choice (checkbox).
  - feedback: What to tell the learner if they respond with option. (Markdown)
- order: Show the answers in a set or random order.
- max_options_to_show: Maximum number of options to present to the user. If the number of options available is less than the max, then all options will be displayed. Otherwise, if order is random, then that number of options will be randomly selected. Or, if order is set, then options will be randomly removed until this requirement is met while preserving order. There will always be at least one correct option presented.

### Number Card

The learner responds with a specific number.

- body: Question. (Markdown)
- options: List of available options
  - value: Number
  - correct: At least one option must be marked as correct. Most number cards will only have one correct option.
  - feedback: What to tell the learner if they respond with option. (Markdown)
- range: A number which means the answer must be plus or minus within this range. For example, if I say the answer is `6`, but the range is `0.01`, then learners may respond between `5.99` and `6.01`.
- default_incorrect_feedback: If none of the options matches the learners response, then the learner will get this feedback. (Markdown)

### Formula Card

Same as the number card, but allows for variables to be present.
TODO combine with number?

- body: Question. (Markdown)
- options: List of available options
  - value: Number
  - correct: At least one option must be marked as correct.
  - feedback: What to tell the learner if they respond with option. (Markdown)
- variables:
  - ???
- range: A number which means the answer must be plus or minus within this range. For example, if I say the answer is `6`, but the range is `0.01`, then learners may respond between `5.99` and `6.01`.
- default_incorrect_feedback: If none of the options matches the learners response, then the learner will get this feedback. (Markdown)

### Match Card

The learner responds with text, and it is checked against text or pattern. This card can represent fill-in-the-blank and short answer types of questions.

- body: Question. (Markdown)
- options: List of available options
  - value: text or pattern (Using standard RegExp in Python)
  - correct: At least one option must be marked as correct.
  - feedback: What to tell the learner if they respond with option. (Markdown)
- default_incorrect_feedback: If none of the options matches the learners response, then the learner will get this feedback. (Markdown)
- case_sensitive: Whether the card forces case sensitivity. Defaults to false.

### Scored Embed Card

TODO

## Peer-Scored Card Kinds

Peer-scored cards require a response from the learner, but are graded by other learners according to the rubric. Learners are notified of their score after receiving sufficient reviews.

### Writing Card

A writing card prompts the learner to write something. Similar in concept to a match card, but it cannot be automatically graded and must be peer reviewed.

- body: Prompt (Markdown)
- max_characters: The maximum number of characters a learner may enter. Defaults to 0, which means no limit.
- rubric:
  - (many) body: Description of the item and expected results.
  - value: How much weight this item gets.
  - scoring: ??? Scoring options for item.

### Record Audio Card

TODO

### Record Video Card

TODO

### Peer-Scored File Card

An upload card prompts the learner to upload something to be peer reviewed.

- body: Prompt (Markdown)
- file_extensions: Kinds of extensions that are allowed, such as documents (txt, md, doc), images (png, jpg), audio (wav, mp3), and video (mov).
- rubric: ???

### Peer-Scored Embed Card

TODO

## Card Tags

- Individual or collaborative.
- Project tags:
  - **Accept**: Provide the learner with a description of the task.
  - **Assess**: Assess the learner's understanding of the task.
  - **Analyze**: Analyze the problem and the context. Brainstorm strategies and pros and cons.
  - **Plan**: Ask the learner to evaluate the task, break it into parts, and form a plan.
  - **Act**: Have learner implement their plan.
  - **Peer Review**: Have the learner evaluate other's work on the same task.
  - **Self Review**: Invite learner to review evaluations of the learner's work.
  - **Reflect**: Invite learner to reflection on project experience.
- Example
- Application
- Motivation
- Comparison
