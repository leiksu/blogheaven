# -*- coding: utf-8 -*-
"""
    Blogheaven
	
    :copyright: (c) 2012 by Xu Lei.
    
"""
import hashlib
from flask import Flask, Response, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from library.core.models import Entry, Tag, User, EntryContent
from library.core.database import db_session
import library.core.config 

app = Flask(__name__)
app.secret_key = library.core.config.SECRET_KEY


# url  routing
@app.errorhandler(404)
def page_not_found(error):
	return 'This page does not exist', 404
	
@app.teardown_request
def shutdown_session(exception=None):
	db_session.remove()

@app.route('/edit/<int:entry_id>', methods=['GET','POST'])
def edit_entry(entry_id=None): 		
	if not current_user.is_authenticated():
		abort(401)

	if entry_id: 
		selected_entry=Entry.query.get(entry_id)		
	else:
		selected_entry = None
		abort(404)
		 
	if request.method == 'POST':
		# update data to database		
		selected_entry.title = request.form['title']
		selected_entry.text = request.form['text']
		db_session.commit()
		
		flash('The post was successfully updated')
		return render_template('show_entries.html', entries=Entry.query.all())
	elif request.method == 'GET':
		# transfer data to form				
		return render_template('show_entries.html', entries=Entry.query.all(), entry_id=entry_id, selected_entry=selected_entry)
		
@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):	
	if not current_user.is_authenticated():
		abort(401)		
		
	db_session.delete(Entry.query.get(entry_id))	
	entry_content_list=EntryContent.query.filter_by(entry_id=entry_id).all()
		
	for index, entry_content_object in enumerate(entry_content_list):		
		for tag_index, tag_object in enumerate(entry_content_object.tag_lists):			
			# delete entries in tags table			
			db_session.delete(Tag.query.get(tag_object.id))	 		
			
		# delete entries in entry_tags table
		db_session.execute('delete from entry_tags where entry_content_id=:entry_content_id', {'entry_content_id':entry_content_object.id})
	
	# delete entries in entry_contents table
	db_session.execute('delete from entry_contents where entry_id=:entry_id', {'entry_id':entry_id})
	db_session.commit()
	
	flash('The post was successfully deleted')
	return redirect(url_for('show_entries'))

@app.route('/')
def show_entries():  
	return render_template('show_entries.html', entries=Entry.query.all() )

@app.route('/show_post/<int:entry_id>')
def show_post(entry_id):  
	return render_template('show_post.html', entry=Entry.query.get(entry_id))

@app.route('/edit_tags/<int:entry_id>', methods=['GET','POST'])
def edit_tags(entry_id=None):	
	if not current_user.is_authenticated():
		abort(401)
		
	tag_arr=request.form['tags'].split(',')	
	tag_list_out=[]
	for index, a in enumerate(tag_arr):		
		a=a.strip()
		if a:
			tag_list_out.append(Tag(a))
			
	entry_content_list=EntryContent.query.filter_by(entry_id=entry_id).all()	
	
	for index, pre_entry_content_object in enumerate(entry_content_list):		
		pre_entry_content_object.active=0
			
	entry_content_object=EntryContent(tag_list_out, entry_id)
	selected_entry=Entry.query.get(entry_id)
	selected_entry.EntryContent=entry_content_object
	db_session.commit()
		
	flash('Tags were successfully updated')
	return render_template('show_entries.html', entries=Entry.query.all() )

	
@app.route('/add', methods=['POST'])
def add_entry():	
	if not current_user.is_authenticated():
		abort(401)
		
	tag_arr=request.form['tags'].split(',')
	
	tag_list_out=[]
	for index, a in enumerate(tag_arr):
		a=a.strip()
		if a:
			tag_list_out.append(Tag(a))
	
	last_entry_object = Entry.query.order_by(Entry.id.desc()).first()
	if last_entry_object: 
		entry_content_object=EntryContent(tag_list_out, last_entry_object.id+1)
	else:
		entry_content_object=EntryContent(tag_list_out, 1)
	
	entry_object=Entry(entry_content_object, request.form['title'], request.form['text'])
	db_session.add(entry_content_object)	
	db_session.add(entry_object)
	db_session.commit()
	
	flash('New post was successfully added')
	return redirect(url_for('show_entries'))
	   

# flask-login
login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
	
@app.route("/login", methods=["GET", "POST"])
def login():
	error = None	
	if request.method == "POST":		
	
        # login and validate the user..
		user = User.query.filter_by(name=request.form["username"]).first()
				
		# check if username is in users table
		if user:
			# check if password is in users table
			if user.password == request.form['password']:
				login_user(user)	
				
				flash('You were logged in')
				return redirect(url_for('show_entries'))
			else:
				error="Invalid password"
		else:
			error="Invalid username"	
		
	return render_template('login.html', error=error)

	
@app.route("/logout")
@login_required
def logout():
    logout_user()	
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
	
    #app.run(debug = library.core.config.DEBUG)
	app.run()