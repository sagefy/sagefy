---
layout: default
title: Technical Architecture
---

This document covers Sagefy's technical architecture. This includes system diagrams, definitions, tools, and high-level decisions. This document does not cover information already in [Setup](/setup), [Technology Stack](/technology-stack), [User Stories](/user-stories) or [Cards & Subjects](/cards-subjects). This document is for new technical contributors and reference.

This document is draft-quality currently. Feel free to suggest edits and improvements!

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

  "https://sagefy.org" -> CloudFlare -> DigitalOcean
  DigitalOcean -> Nginx [lhead=cluster0]

  subgraph cluster0 {
    label="Docker Compose\non Ubuntu Server"
    client [label="Node.js Client\nExpress, React"]
    server [label="Node.js Server\nExpress, Postgraphile"]
    db [label="PostgreSQL\nvia dbmate"]
    Nginx -> client -> server -> db
  }

  server -> Mailgun
}
-->

<svg width="223pt" height="688" viewBox="0 0 223.33 516" xmlns="http://www.w3.org/2000/svg"><g class="graph" transform="translate(4 512)"><path fill="#fff" stroke="transparent" d="M-4 4v-516h223.33V4H-4z"/><g class="cluster"><path fill="none" stroke="#eee" d="M8-8v-312h143V-8H8z"/><text text-anchor="middle" x="79.5" y="-301.6"  font-size="18" fill="#222">Docker Compose</text><text text-anchor="middle" x="79.5" y="-283.6"  font-size="18" fill="#222">on Ubuntu Server</text></g><g class="node"><text text-anchor="middle" x="83" y="-486.4"  font-size="12" fill="#333">https://sagefy.org</text></g><g class="node"><text text-anchor="middle" x="83" y="-414.4"  font-size="12" fill="#333">CloudFlare</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M83-471.7v25.59"/><path fill="#ccc" stroke="#ccc" d="M86.5-446.1l-3.5 10-3.5-10h7z"/></g><g class="node"><text text-anchor="middle" x="83" y="-342.4"  font-size="12" fill="#333">DigitalOcean</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M83-399.7v25.59"/><path fill="#ccc" stroke="#ccc" d="M86.5-374.1l-3.5 10-3.5-10h7z"/></g><g class="node"><text text-anchor="middle" x="83" y="-246.4"  font-size="12" fill="#333">Nginx</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M83-327.76v.46"/><path fill="#ccc" stroke="#ccc" d="M86.5-330L83-320l-3.5-10h7z"/></g><g class="node"><text text-anchor="middle" x="83" y="-180.4"  font-size="12" fill="#333">Node.js Client</text><text text-anchor="middle" x="83" y="-168.4"  font-size="12" fill="#333">Express, React</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M83-231.7v25.59"/><path fill="#ccc" stroke="#ccc" d="M86.5-206.1l-3.5 10-3.5-10h7z"/></g><g class="node"><text text-anchor="middle" x="83" y="-108.4"  font-size="12" fill="#333">Node.js Server</text><text text-anchor="middle" x="83" y="-96.4"  font-size="12" fill="#333">Express, Postgraphile</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M83-159.7v25.59"/><path fill="#ccc" stroke="#ccc" d="M86.5-134.1l-3.5 10-3.5-10h7z"/></g><g class="node"><text text-anchor="middle" x="83" y="-36.4"  font-size="12" fill="#333">PostgreSQL</text><text text-anchor="middle" x="83" y="-24.4"  font-size="12" fill="#333">via dbmate</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M83-87.7v25.59"/><path fill="#ccc" stroke="#ccc" d="M86.5-62.1l-3.5 10-3.5-10h7z"/></g><g class="node"><text text-anchor="middle" x="187" y="-30.4"  font-size="12" fill="#333">Mailgun</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M108.44-87.88c13.35 8.99 29.88 20.12 44.34 29.85"/><path fill="#ccc" stroke="#ccc" d="M155.12-60.68l6.34 8.49-10.25-2.68 3.91-5.81z"/></g></g></svg>

## Database

Sagefy depends on PostgreSQL. Most of Sagefy's function is completely in PostgreSQL. We use PostgreSQL thoroughly, including: schemas, enums, comments, composed types, functions, triggers, indexes, foreign key relationships, views, common table expressions, recursion, joins, PLPGSQL, notifications, full-text search, constraints, access policies, and row-based access control.

You can view the PostgreSQL specific files in the `postgres/` folder. We use [dbmate](https://github.com/amacneil/dbmate) to maintain database migrations. dbmate automatically generates the latest schema in `schema.sql`. Sagefy's database runs on port 2600. We also use the [postgres-json-schema](https://github.com/gavinwahl/postgres-json-schema) extension for some validations.

### Tables and relations

A full list of tables and relations is in `postgres/schema.sql`.

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

  user
  subject -> user
  subject -> subject
  card -> subject
  card -> user
  response -> card
  response -> subject
  response -> user
  user_subject -> subject
  user_subject -> user
  topic -> user
  topic -> card
  topic -> subject
  post -> user
  post -> card
  post -> subject
  post -> topic
}
-->

<svg width="322pt" height="332pt" viewBox="0 0 322.19 332" xmlns="http://www.w3.org/2000/svg"><g class="graph" transform="translate(4 328)"><path fill="#fff" stroke="transparent" d="M-4 4v-332h322.19V4H-4z"/><g class="node"><text text-anchor="middle" x="137" y="-14.4" font-size="12" fill="#333">user</text></g><g class="node"><text text-anchor="middle" x="137" y="-86.4" font-size="12" fill="#333">subject</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M137-71.7v25.59"/><path fill="#ccc" stroke="#ccc" d="M140.5-46.1l-3.5 10-3.5-10h7z"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M164.24-103.49C174.02-103.78 182-99.28 182-90c0 5.8-3.12 9.73-7.84 11.79"/><path fill="#ccc" stroke="#ccc" d="M174.69-74.75l-10.45-1.76 9.27-5.14 1.18 6.9z"/></g><g class="node"><text text-anchor="middle" x="82" y="-158.4" font-size="12" fill="#333">card</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M79-143.82c-1.84 14.49-2.84 35.55 3 52.82"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M95.6-143.7c6.52 8.31 14.47 18.42 21.65 27.56"/><path fill="#ccc" stroke="#ccc" d="M120.13-118.13l3.43 10.03-8.93-5.71 5.5-4.32z"/></g><g class="node"><text text-anchor="middle" x="139" y="-230.4" font-size="12" fill="#333">response</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M137-161c-7.72 38.81-67.68 32.52-55 70M140.1-215.85c.53 14.28.43 35.08-3.1 52.85"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M137-161c-2.76 13.87-3.01 29.61-2.46 42.63"/><path fill="#ccc" stroke="#ccc" d="M138.05-118.35l-2.9 10.19-4.09-9.77 6.99-.42z"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M124.91-215.7c-6.83 8.4-15.17 18.63-22.67 27.84"/><path fill="#ccc" stroke="#ccc" d="M104.96-185.65l-9.03 5.55 3.6-9.97 5.43 4.42z"/></g><g class="node"><text text-anchor="middle" x="241" y="-158.4" font-size="12" fill="#333">user_subject</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M307-89c-19.78 50.96-89.18 65.07-132.96 68.82"/><path fill="#ccc" stroke="#ccc" d="M174.27-16.69l-10.22-2.77 9.72-4.21.5 6.98z"/><path fill="none" stroke="#ccc" d="M275.46-143.79c20.05 12.64 39.88 31.3 31.54 52.79"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M215.56-143.88c-13.35 8.99-29.88 20.12-44.34 29.85"/><path fill="#ccc" stroke="#ccc" d="M172.79-110.87l-10.25 2.68 6.34-8.49 3.91 5.81z"/></g><g class="node"><text text-anchor="middle" x="27" y="-230.4" font-size="12" fill="#333">topic</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M82-89c5.73 16.93 17.51 32.86 28.7 45.22"/><path fill="#ccc" stroke="#ccc" d="M113.56-45.85l4.34 9.66-9.42-4.84 5.08-4.82z"/><path fill="none" stroke="#ccc" d="M27-161c16.37 36.02 42.32 32.52 55 70M23.17-215.76c-2.4 14.7-3.76 36.05 3.83 52.76"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M27-161c7.12 15.67 44.59 37.42 73.84 52.5"/><path fill="#ccc" stroke="#ccc" d="M102.66-111.5l7.34 7.64-10.5-1.4 3.16-6.24z"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M40.6-215.7c6.52 8.31 14.47 18.42 21.65 27.56"/><path fill="#ccc" stroke="#ccc" d="M65.13-190.13l3.43 10.03-8.93-5.71 5.5-4.32z"/></g><g class="node"><text text-anchor="middle" x="82" y="-302.4" font-size="12" fill="#333">post</text></g><g class="edge"><path fill="none" stroke="#ccc" d="M251-233c34.82 58.22 80.55 78.75 56 142"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M251-233c17.04 30.11-34.83 26.45-57 53-16.5 19.76-32.03 44.59-42.71 63"/><path fill="#ccc" stroke="#ccc" d="M154.31-115.23l-7.99 6.96 1.91-10.42 6.08 3.46z"/><path fill="none" stroke="#ccc" d="M109.09-303.23C148.83-298.98 221.41-284.47 251-235"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M82-287.87v97.48"/><path fill="#ccc" stroke="#ccc" d="M85.5-190.19l-3.5 10-3.5-10h7z"/></g><g class="edge"><path fill="none" stroke="#ccc" d="M68.4-287.7c-6.52 8.31-14.47 18.42-21.65 27.56"/><path fill="#ccc" stroke="#ccc" d="M49.37-257.81l-8.93 5.71 3.43-10.03 5.5 4.32z"/></g></g></svg>

The _user_ table is actually two: one that is public information, and one that is private information. This table is only logged in users.

Subjects are in the `subject_version` table. `subject_version` relate to either logged in user or logged out session. Two additional tables, `subject_version_before_after` and `subject_version_parent_child`, are join tables. There is also tables `entity`, `entity_version`, and `subject_entity`, which Sagefy uses for maintaining foreign key relationships.

Cards are similarily in the `card_version` table. A `card_entity` table maintains foreign key relationships.

The `user_subject` table stores the intent to learn for users. The table may relate to logged in user or logged out session.

`topic`s are a single table. Topics relate to logged into user or logged out session. Topics belong to subjects and cards.

`post`s are two tables: `post`. Posts relate to logged in user or logged out session. Posts may be post, proposal, or vote. The proposal kind joins with card and subject versions via the `post_entity_version` table.

### Running migrations

We use dbmate to run migrations. New migrations are with `npm run dbmate new "name"`, and updates are with `npm run dbmate up`.

## Postgraphile service

What makes the Sagefy PostgreSQL database useful with little custom code is [Postgraphile](https://www.graphile.org/postgraphile/). Postgraphile parses the full PostgreSQl schema and turns it into a GraphQL API. Sagefy follows the advice found in their [PostgresQL schema design](https://www.graphile.org/postgraphile/postgresql-schema-design/) for PostgreSQL design. This service runs on port 2601. The service reads your `.env` file, so take care to configure per environment.

We extend Postgraphile and Express here slightly to send emails. We listen to notifications from PostgreSQL, and the service then responds by sending email contents to the Mailgun transactional email service.

You can interact with this service directly on local development at `https://localhost:2601/graphiql`. The service is self-documenting.

Tests in this directory check both the PostgreSQL schema for correct function as well as the translation to GraphQL.

[pm2](https://pm2.keymetrics.io/) manages the Node.js process.

## Web client

Sagefy's web client runs on port 2602. It is a Node.js server with Express. We store a JWT cookie on the client from this service.

The URLs roughly follow a "REST"-like pattern. Most endpoint run a single GraphQL query to the Postgraphile service, format the results slightly, and render HTML with server-side only React.

We have no client-side, in-browser JavaScript. We use plain HTML forms quite often.

There is also minimal CSS, using [`drab.css`](https://github.com/heiskr/drab.css) and a few small extensions. The CSS can be rebuilt with `npm run prepublish`, though the need is rare. There are very few classes, preferring simple HTML tags automatically styled.

There's a folder of GraphQL queries. They are separate because the `server/` directory uses the actual client queries to run tests. This avoids duplication.

The top level files in the `views/` directory are all pages. A subfolder of `components/` are smaller React views shared between multiple pages.

[pm2](https://pm2.keymetrics.io/) manages the Node.js process.

## Nginx

Nginx is the only piece that has direct access to the public internet. So we run Nginx on port 80. In addition to routing traffic to the Node.js client service, we also serve some static files directly with Nginx. We take advantage of Nginx's rate limiting features.

## Logging, monitoring, reporting, and alerting

We monitor the up status of the Sagefy with Freshping.

TBD

## Testing and continuous integration

We run tests on every commit and pull request with CircleCI.

Our test suite runs Jest, Eslint, Supertest, and Joi. Prettier runs with each commit for code formatting.

## Deployment

This is a manual process currently, `ssh`ing into the server, `cd` into the sagefy directory, and running `script/deploy.sh`.
