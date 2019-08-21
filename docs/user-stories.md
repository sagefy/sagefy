---
layout: default
title: User Stories
---

This document serves as a list of major use cases for Sagefy's functionality. We can use the document to test and review functionality. This document does not cover every edge case.

## Logged Out

- When I go to a messy URL, I get a 404.
- When I don't have a JWT cookie, visiting a page creates one.
- I can view the contact page.
- I can view the terms page.
- I can view the sitemap.
- When I visit the home page, I see a list of popular subjects, the logged out footer, and I can search.
- When I search subjects for "Music", I get results.
- When I search subjects for a new term, I don't get results, but I get the option to create a subject.
- When I create a subject on the search subjects page, it creates the subject and redirects me back to the search.
- When I create a subject on the create subject page, ditto.
- I can visit a subject page.
- I can visit the subject talk page.
- On the subject talk page, I can create a new topic.
- On the subject talk page, I can create a new post.
- I can view the subject history page.
- I can edit the subject, and see the change on the subject history page. It maintains the parents and befores.
- I visit a card page.
- I can make a topic on the card talk page.
- I can make a post on the card talk page.
- I can view the card history page.
- I can view a user page.
- When I try to learn a subject with no cards, I'm taken to the create card page.
- I can create a choice card.
- I can create a video card.
- I can create a page card.
- I can create an unscored embed card.
- When I choose to learn a subject with cards but no child subjects, I'm taken to learn those cards.
- I can watch a video card.
- I can read a page card.
- I can play an embed card.
- I can parse a choice card.
- I can submit a response to a choice card.
- When I reach a sufficient percentage, I complete the subject and go back to search.
- :( When I choose to learn a subject with child subjects, I go to the choose step page.
- :( When I reach a sufficient percentage, I go to the next subject.

## Logged In

- I can sign up for a new account.
- I can view my dashboard.
- I can log out of my account.
- When I try to sign up for a duplicate account, I see error messages.
- I can log in to my account with the right password.
- I get an error message if I try to log in with the wrong password.
- I can add a subject to my dashboard.
- When I visit the home page, I see the logged in footer.
- When I create a subject on the search subjects page, it creates the subject and takes me to my dashboard.
- When I create a subject on the create subject page, ditto.
- I can change my name on the settings page.
- I can change my password. I get an email my password changed.
- I can change my email. I get an email my email changed.
