---
layout: default
title: Technical Architecture
---

This document covers Sagefy's technical architecture. This includes system diagrams, definitions, tools, and high-level decisions. This document does not cover information already in [Setup](/setup), [Technology Stack](/technology-stack), [User Stories](/user-stories) or [Cards & Subjects](/cards-subjects). This document is for new technical contributors and reference.

## System diagram

<!--
digraph workflow {
  concentrate=true
  compound=true

  graph [
    fontsize=18
    fontcolor="#222222"
    color="#eeeeee"
  ]
  node [
    fontsize=12
    fontcolor="#333333"
    color="#dddddd"
    shape="plaintext"
  ]
  edge [
    fontsize=10
    color="#cccccc"
    fontcolor="#666666"
  ]

  PostgreSQL
    dbmate
  Node.js-Server
    Postgraphile
    Mailgun
  Node.js-Client
    React
    Express
    Drab.css
    Feather-Icons
  Nginx
  Docker-Compose on Ubuntu
  DigitalOcean
  CloudFlare
}
-->

<style>svg{max-width:100%;}</style>

TBD

## Database

TBD

### Tables and relations

TBD

### Running migrations

TBD

### Database differences in local, test, continuous integration, and production

TBD

## Postgraphile service

[PostgresQL schema design](https://www.graphile.org/postgraphile/postgresql-schema-design/)

TBD

## Web client

TBD

## Nginx

TBD

## Logging, monitoring, reporting, and alerting

Freshping

TBD

## Testing and continuous integration

TBD

Jest
Supertest
Joi
Eslint
Prettier
CircleCi

## Deployment

TBD
