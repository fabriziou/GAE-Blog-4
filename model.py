import datetime
import logging

from google.appengine.api import users
from google.appengine.ext import db

import defines

class Comment(db.Model):
	author = db.UserProperty()
	content = db.TextProperty()
	comment_time = db.DateTimeProperty(auto_now_add = True)
	id = db.IntegerProperty()
	
class Article(db.Model):
	title = db.StringProperty()
	content = db.TextProperty()
	is_draft = db.BooleanProperty()
	published_time = db.DateTimeProperty(auto_now_add = True)
	last_modified_time = db.DateTimeProperty(auto_now_add = True)
	comments = db.ListProperty(db.Key)
	comment_counter = db.IntegerProperty()
	id = db.IntegerProperty()

	@classmethod
	def get(cls, id):
		q = Article.all()
		q.filter('id = ', int(id))
		return q.get()
		
	@classmethod
	def get_by_title(cls, title):
		q = Article.all()
		q.filter('title = ', title)
		return q.get()
	
	@classmethod
	def get_all(cls, order='-published_time'):
		q = Article().all()
		q.order(order)
		return q.fetch(defines.FETCH_ALL)
	
	@classmethod
	def get_all_published(cls, order='-published_time'):
		q = Article().all()
		q.filter('is_draft = ', False)
		q.order(order)
		return q.fetch(defines.FETCH_ALL)
	
	@classmethod
	def delete_article(cls, id):
		comments = db.get(Article.get(id).comments)
		for c in comments:
			c.delete()
		Article.get(id).delete()
		
	@classmethod
	def save_comment(cls, article, content):
		c = Comment()
		c.author = users.get_current_user()
		c.content = content
		c.put()
		c.id = c.key().id()
		c.put()
				
		article.comments.append(c.key())
		article.comment_counter = article.comment_counter + 1
		article.put()
		
	@classmethod
	def delete_comment(cls, article, comment):
		article.comments.remove(comment.key())
		article.comment_counter = article.comment_counter - 1
		article.put()
		comment.delete()
		
	@classmethod
	def get_comments(cls, article):
		comments = db.get(article.comments)
		return comments
		
	@classmethod
	def get_comment(cls, article, id):
		comments = Article.get_comments(article)
		for c in comments:
				if c.id == id:
					return c
	
	def save(self, 
			title='', 
			content='', 
			is_draft=True,
			last_modified_time=datetime.datetime.now() + datetime.timedelta(hours=+8)):
		# if self.id exist means the article is already exsit, then update it,
		# or create a new article.
		if self.id:
			a = Article().get(self.id)
			a.title = title
			a.content = content
			a.is_draft = is_draft
			# no modifying published time
			a.last_modified_time = last_modified_time
			a.id = self.id

			a.put()
		else:
			self.title = title
			self.content = content
			self.is_draft = is_draft
			self.published_time = datetime.datetime.now() + datetime.timedelta(hours=+8) # for solving time zone problem
			self.last_modified_time = last_modified_time
			self.comment_counter = 0

			self.put()
			self.id = self.key().id()
			self.put()