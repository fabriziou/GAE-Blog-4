import logging
import os
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import defines
from model import *

class BlogHandler(webapp.RequestHandler):
	def render_template(self, 
		sub_dir=defines.PAGES_SUB_DIR,
	 	page=None, 
		template_values=[]):
		path = os.path.join(os.path.dirname(__file__), sub_dir, page)
		self.response.out.write(template.render(path, template_values))
	
	def is_admin(self):
		if users.is_current_user_admin():
			return True
		else:
			tv = {
				'defines' : defines
			}
			self.render_template(page=defines.PAGES['not_admin'], template_values=tv)
		return False
		
	def save_article(self, request):
		draft = str(request.get('is_draft'))
		bool_draft = True
		if draft == 'False':
			bool_draft = False
		# if python raise a ValueError means it's a new article
		# no raising means the article already exsit
		try:
			a = Article().get(int(request.get('article_id')))
			a.save(
					title = request.get('title'),
					content = request.get('content'),
					is_draft = bool_draft
				  )
		except ValueError:
			a = Article()
			a.save(
					title = request.get('title'),
					content = request.get('content'),
					is_draft = bool_draft
				)
		return a.key().id()
		

class PageIndexRequest(BlogHandler):
	def get(self):
		tv = {
			'articles' : Article().get_all_published(),
			'defines' : defines,
			'users' : users,
		}
		
		self.render_template(page=defines.PAGES['index'], template_values=tv)

class PageSingleArticleRequest(BlogHandler):
	def get(self, article_id):
		tv = {
			'article' : Article().get(int(article_id)),
			'comments' : Article.get_comments(Article.get(int(article_id))),
			'users' : users,
			'defines' : defines,
		}
		self.render_template(page=defines.PAGES['single_article'], template_values=tv)
		
class CommentSubmitRequest(BlogHandler):
	def post(self):
		Article.save_comment(
			Article.get(int(self.request.get('article_id'))),
			self.request.get('content')
			)
		self.redirect('/article/' + self.request.get('article_id'))
		
class CommentDeleteRequest(BlogHandler):
	def get(self, article_id, comment_id):
		if self.is_admin():
			a = Article.get(int(article_id))
			c = Article.get_comment(a, int(comment_id))
			Article.delete_comment(a, c)
			self.redirect('/article/' + article_id)

class PageNotFoundRequest(BlogHandler):
	def get(self):
		self.render_template(page='not_found.html')

class RssFeedRequest(BlogHandler):
	def get(self):
		tv = {
			'articles' : Article().get_all(),
			'defines' : defines,
			'url' : 'http://' + self.request.environ['SERVER_NAME'] + ':' + self.request.environ['SERVER_PORT'],
			'last_update' : datetime.datetime.now(),
		}
		self.response.headers['Content-Type'] = 'text/xml'
		self.render_template(page='rss.xml', template_values=tv)
		

#	=====
#	main
#	=====

application = webapp.WSGIApplication([
	('/', PageIndexRequest),
	(r'/article/(.*)', PageSingleArticleRequest),
	('/comment/submit', CommentSubmitRequest),
	(r'/comment/delete/(.*)/(.*)', CommentDeleteRequest),
	('/rss', RssFeedRequest),
	('/.*$', PageNotFoundRequest)
	], debug = True)
	
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()