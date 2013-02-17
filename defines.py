import sys
from google.appengine.api import users

PAGES_SUB_DIR = 'pages'

"""
	it seems python on gae environment is 32 bit
	so we need a solution to make it works
	or python will raise an error
"""
FETCH_ALL = sys.maxint / 2**32 - 1

URLS = {
	#request
	'main' : '/',
	'not_found' : '/.*$',
	'one_article' : '/article/?',
	'comment_submit' : '/comment/submit',
	'comment_delete' : '/comment/delete?',
	
	#admin request
	'admin' : '/admin',
	'article_edit' : '/admin/article/edit/?',
	'article_save' : '/admin/article/save',
	'article_delete' : '/admin/article/delete',
	'article_preview' : '/admin/article/preview',
}

PAGES = {
	'index' : 'index.html',
	'admin' : 'admin.html',
	'article_edit' : 'extends_admin_edit.html',
	'not_admin' : 'not_admin.html',
	'not_found' : 'not_found.html',
	'single_article' : 'single_article.html'
}

BLOG = {
	'blog_name' : 'Code for Food',
	'blog_desc' : 'this is my blog!',
	'blog_author' : 'zushenyan'
}

def get_login_url():
	if users.get_current_user():
		login_url = users.create_logout_url('/')
	else:
		login_url = users.create_login_url('/')
	return login_url