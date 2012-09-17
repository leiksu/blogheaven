from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, backref


from database import Base

import config 
 

entry_tags = Table('entry_tags', Base.metadata,
	Column('entry_content_id', Integer, ForeignKey('entry_contents.entry_content_id')),
    Column('tag_id', Integer, ForeignKey('tags.tag_id'))
)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column('tag_id',Integer, primary_key=True)
    name = Column('name',String(50))
    	
    def __init__(self, name=None):
        self.name = name        

    def __repr__(self):
        return '<Tag %r>' % (self.name)	
		
class Entry(Base):
	__tablename__ = 'entries'
	id = Column('entry_id',Integer, primary_key=True)	
	
	title = Column('title',String(50))
	text = Column('text',String(120)) 
	
	entry_content_id = Column('entry_content_id',Integer, ForeignKey('entry_contents.entry_content_id'))	
	EntryContent = relationship('EntryContent',
        backref=backref('Entry', lazy='dynamic'))
	
	def __init__(self, EntryContent=None, title=None, text=None):
		self.EntryContent = EntryContent
		self.title = title
		self.text = text
		
		
	def __repr__(self):
		return '<Entry %r>' % (self.title)
		
class EntryContent(Base):
	__tablename__ = 'entry_contents'
	id = Column('entry_content_id',Integer, primary_key=True)	
	entry_id = Column('entry_id',Integer, default=0)	
	active = Column('active', Integer)
	tag_lists = relationship('Tag', secondary = entry_tags, 
			backref = backref('entrie_lists',lazy='dynamic'))
			
	def __init__(self, tag_lists, entry_id=None, active=True):
		self.entry_id = entry_id
		self.active = active	
		self.tag_lists = tag_lists
		
	def __repr__(self):
		return '<EntryContent %d>' % (self.id)
		

class User(Base):
	__tablename__ = 'users'
	id = Column('user_id',Integer, primary_key=True)
	name = Column('name',String(50), unique=True)
	password = Column('password',String(50)) 
	active = Column('active',Integer) 
	
	def __init__(self, id, name, password, active = True):
		self.id = id
		self.name = name
		
		self.password = password   
		self.active = active		
        
		
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return unicode(self.id)
		
	def __repr__(self):
		return '<User %s>' % (self.name)
