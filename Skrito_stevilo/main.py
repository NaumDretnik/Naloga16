#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


class SkritoHandler(BaseHandler):
    def post(self):
        skrito_stevilo = 85
        ugibanje = int(self.request.get("ugibanje"))
        if ugibanje == skrito_stevilo:
            return self.write("Bravo, uganili ste skrito število in zadeli 1.000 evrov.")
        else:
            return self.write("<p>Žal, " + str(ugibanje) + " ni skrito število. Več sreče prihodnjič.<p> <button><a href=\"/\">Poskusite še enkrat</a></button>")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/skrito', SkritoHandler),

], debug=True)
