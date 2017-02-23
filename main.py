import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **param):
        t = jinja_env.get_template(template)
        return t.render(**param)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blogs(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_front(self, subject ="", content="", error=""):
        blogs = db.GqlQuery("SELECT * from Blogs ORDER BY created desc")
        self.render("blogDisplay.html", blogs= blogs)
    def get(self):
        self.render_front()


class NewPost(Handler):
    def render_newPost(self, subject="", content="", error=""):
        self.render("blogTemplate.html", subject=subject, content=content, error=error)
    def get(self):
        self.render_newPost()
    def post(self):
        subject= self.request.get("subject")
        content=  self.request.get("content")
        if subject and content:
            a = Blogs(subject= subject, content=content)
            key = a.put()
            redirect_id = key.id()
            #lastBlog = db.GqlQuery("SELECT subject, content from Blogs ORDER BY created")
            self.redirect('/blog/%s' % str(redirect_id))
        else:
            error= "Both title and blog are needed"
            self.render_newPost(subject=subject, content=content, error=error)

class BlogId(Handler):
    def get(self, post_id):
        postById = Blogs.get_by_id(int(post_id))
        #post = Blogs.get(postById)
        #self.response.out.write(postById)
        print postById
        # if postId :
        #self.render("permalink.html", postById = post)
        # self.response.out.write("You landed at the right page")

app = webapp2.WSGIApplication([('/', MainPage),
                                ('/newPost', NewPost),
                                ('/blog/([0-9]+)',BlogId )
                                ], debug= True)
#
# app = webapp2.WSGIApplication([
#         webapp2.Route(r'/', handler=MainPage, name='home'),
#         webapp2.Route(r'/newPost', handler=NewPost, name='newPost'),
#         webapp2.Route(r'/blog/<post_id:([0-9]+)>', handler=BlogId, name='blog-id'),
# ])

#('/blog/<post_id:([0-9]+)>', BlogId)
