---
title: RESTish
layout: default
---

General REST principles, but made more practical.

- Use nouns.
- Plural nouns.
- All lowercase.
- Concrete is better than abstract.
- Parent noun, id, child noun, id...
- ID can be reference.
    - Current, recent...
- GET one, GET many, POST (create), PUT (update), PATCH, DELETE, OPTIONS
- Everything else in query string.
    - Search, sort, filter, fields (embed), paginate...
- Verbose errors. One for devs, one for users.
- Use HTTP status codes.
- Use SSL.
- Version at beginning of URL.
- Content type as extension if not JSON.
- JSON is default.
- Use pagination (limit, offset) and optional field params.
- If no resource, pseudo resource or root level verb.
- Fields in lower camelCase.
- method=x with POST for PUT, PATCH, and DELETE.
- Updates should return object as well.
- Use OAuth latest.
- Stateless except for authorization.
- No root level arrays.
- Wrap objects in type of object.
- Include links to related requests. [RFC5988](http://tools.ietf.org/html/rfc5988)
- Autodoc everything.
- Cache everything.
- Gzip everything.
- Provide full resources.
- Use ISO8601 for dates and times.
- Implement the options verb.
- Aim for orthogonal.
- Use [response codes](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html).

References
----------

- http://info.apigee.com/Portals/62317/web%20api.pdf
- http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
- https://google-styleguide.googlecode.com/svn/trunk/jsoncstyleguide.xml
- http://www.slideshare.net/mario_cardinal/best-practices-for-designing-pragmatic-restful-api
- https://github.com/interagent/http-api-design
