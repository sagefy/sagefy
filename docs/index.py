#!/usr/bin/env python

import sys
import os
import webapp2
import jinja2

approot = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(approot, 'libraries'))
from markdown2 import markdown

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader('%s/templates' % approot)
)


def html(doc_slug):
    content = markdown(open('%s/pages/%s.md' % (
        approot,
        doc_slug
    )).read())
    aside = markdown(open('%s/pages/_sidebar.md' % approot).read())
    template = jinja_environment.get_template('index.html')
    return template.render({
        'doc_slug': doc_slug,
        'content': content,
        'aside': aside,
    })


class PageHandler(webapp2.RequestHandler):
    def get(self, doc_slug):
        self.response.out.write(html(doc_slug))


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(html('index'))


app = webapp2.WSGIApplication([
    webapp2.Route('/docs/<doc_slug>', handler=PageHandler),
    webapp2.Route('/docs', handler=IndexHandler),
    webapp2.Route('/', handler=IndexHandler)
], debug=True)
