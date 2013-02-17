from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app

from model import *
import defines
import request

class PageAdminRequest(request.BlogHandler):
	def get(self):
		if self.is_admin():
			tv = {
				'articles' : Article.get_all(),
				'defines' : defines
			}
			self.render_template(page=defines.PAGES['admin'], template_values=tv)

class PageAdminEditRequest(request.BlogHandler):
	def get(self, article_id):
		if self.is_admin():
			tv = {
				'article' : None,
				'defines' : defines,
				'server_name' : self.request.environ['SERVER_NAME'],
				'server_port' : self.request.environ['SERVER_PORT'],
			}
			if article_id:
				a = Article.get(article_id)
				tv['article'] = a
				self.render_template(page=defines.PAGES['article_edit'], template_values=tv)
			else:
				self.render_template(page=defines.PAGES['article_edit'], template_values=tv)
				
class ArticleSaveRequest(request.BlogHandler):
	def post(self):
		if self.is_admin():
			self.save_article(self.request)
			self.redirect('/admin/article/edit/' + self.request.get('article_id'))

class ArticleDeleteRequest(request.BlogHandler):
	def get(self, article_id):
		if self.is_admin():
			Article.delete_article(int(article_id))
			self.redirect('/admin')
			
class ArticlePreviewRequest(request.BlogHandler):
	def post(self):
		if self.is_admin():
			id = self.save_article(self.request)
			self.redirect('/admin/article/edit/' + str(id))
		
#	===
#	main
#	===

application = webapp.WSGIApplication([
	('/admin', PageAdminRequest),
	(r'/admin/article/edit/(.*)', PageAdminEditRequest),
	('/admin/article/save', ArticleSaveRequest),
	(r'/admin/article/delete/(.*)', ArticleDeleteRequest),
	('/admin/article/preview', ArticlePreviewRequest),
	('/admin/.*$', request.PageNotFoundRequest)
	],debug = True)
	
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()