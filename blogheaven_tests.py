# -*- coding: utf-8 -*-
"""
    Blogheaven Tests
    
    Tests the Blogheaven application.

    :copyright: (c) 2012 by Xu Lei.    
"""
import os
import blogheaven
import unittest
import tempfile
import library.core.config
import library.core.database
import library.core.models
from library.core.database import db_session
from library.core.models import User

class BlogheavenTestCase(unittest.TestCase):


	def setUp(self):
		"""Before each test, set up a blank database"""
		
		self.db_fd, library.core.config.DB_URI = tempfile.mkstemp()
		library.core.config.TESTING = True
		self.app = blogheaven.app.test_client()
		
		library.core.database.init_db()
		
		last_user_object = User.query.order_by(User.id.desc()).first()		
		if last_user_object:
			admin = User(last_user_object.id+1, last_user_object.id+1, 'default')
		else: 
			admin = User(1, 'leiksu', 'default')			
		db_session.add(admin)
		db_session.commit()

	def tearDown(self): 
		"""Get rid of the database again after each test."""
		os.close(self.db_fd)
		os.unlink(library.core.config.DB_URI)
		
	def login(self, username, password): 
		return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)
		
		
	def logout(self):
		return self.app.get('/logout', follow_redirects=True)
			
		
	# testing functions

	def test_empty_db(self):
		"""Start with a blank database."""
		rv = self.app.get('/')
		assert 'No posts here so far' in rv.data


	def test_login_logout(self):
		"""Make sure login and logout works"""
		rv = self.login(library.core.config.USERNAME,
						library.core.config.PASSWORD)
		
		assert 'You were logged in' in rv.data
		rv = self.logout()
		assert 'You were logged out' in rv.data
		rv = self.login(library.core.config.USERNAME + 'x',
						library.core.config.PASSWORD)
		assert 'Invalid username' in rv.data
		rv = self.login(library.core.config.USERNAME,
						library.core.config.PASSWORD + 'x')
		assert 'Invalid password' in rv.data

	def add_post(self, title, tags, text):
		"""Adds a post"""
        
		rv = self.app.post('/add', data=dict(
				title=title,
				tags=tags,
				text=text
			), follow_redirects=True)
		
		if title:
			assert 'New post was successfully added' in rv.data
		return rv
		
	def test_adding_post(self):
		"""Test that adding post work"""
		
		self.login(library.core.config.USERNAME,
					library.core.config.PASSWORD)
		
		
		title='<Hello>'
		tags='<dfdf,tyut,  tyrty>'
		text='<strong>HTML</strong> allowed here'
		
		rv = self.add_post(title, tags, text)		
		#print rv
		assert 'No posts here so far' not in rv.data
		assert '&lt;Hello&gt;' in rv.data
		assert '<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
