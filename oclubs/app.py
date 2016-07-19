#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#

from __future__ import absolute_import, unicode_literals

from flask import (
    Flask, redirect, request, render_template, url_for, session, jsonify, g, abort
)

import traceback

import oclubs
from oclubs.access import database
from oclubs.userblueprint import userblueprint
from oclubs.clubblueprint import clubblueprint
from oclubs.actblueprint import actblueprint

from oclubs.redissession import RedisSessionInterface

app = Flask(__name__)

app.register_blueprint(userblueprint, url_prefix='/user')
app.register_blueprint(clubblueprint, url_prefix='/club')
app.register_blueprint(actblueprint, url_prefix='/act')

app.session_interface = RedisSessionInterface()


def get_name():
    '''Get user's name if available'''
    if 'user_id' in session:
        user_obj = g.get('user_obj', None)
        if not user_obj:
            user_obj = oclubs.objs.User(session['user_id'])
            g.user_obj = user_obj
        user = user_obj.nickname
    else:
        user = ''
    return user


def get_picture(picture):
    return url_for('static', filename='images/' + picture + '.jpg')


app.jinja_env.globals['usernickname'] = get_name
app.jinja_env.globals['getpicture'] = get_picture


@app.after_request
def database_done(response):
    if response.status_code < 400:
        database.done(True)
    else:
        database.done(False)
    return response


@app.errorhandler(404)
@app.route('/404')
def page_not_found(e):
    '''Wrong url'''
    return render_template('error.html',
                           title='404 Page Not Found',
                           is_page_not_found=True
                           ), 404


@app.errorhandler(403)
def forbidden(e):
    '''No access'''
    return render_template('error.html',
                           title='403 Forbidden',
                           is_forbidden=True
                           ), 403


@app.errorhandler(401)
def unauthorized(e):
    '''Not logged in'''
    return render_template('error.html',
                           title='401 Unauthorized',
                           is_unauthorized=True
                           ), 401


@app.errorhandler(500)
def internal_server_error(e):
    '''Internal server error'''
    return render_template('error.html',
                           title='500 Internal Server Error',
                           is_internal_server_error=True
                           ), 500


@app.route('/login', methods=['POST'])
def login():
    '''API to login'''
    if 'user_id' in session:
        status = 'loggedin'
    else:
        user = oclubs.objs.User.attempt_login(
            request.form['username'],
            request.form['password']
        )
        if user is not None:
            session['user_id'] = user.id
            status = 'success'
        else:
            status = 'failure'
    return jsonify({'result': status})


@app.route('/')
def homepage():
    '''Homepage'''
    # Three excellent clubs
    ex_clubs = [{'name': 'Website Club', 'picture': '1', 'intro': 'We create platform for SHSID.'},
                {'name': 'Art Club', 'picture': '2', 'intro': 'We invite people to the world of arts.'},
                {'name': 'Photo Club', 'picture': '3', 'intro': 'We search for the beauty in this world.'}]
    return render_template('homepage.html',
                           title='Here you come',
                           is_home=True,
                           ex_clubs=ex_clubs)


@app.route('/about')
def about():
    '''About This Website'''
    return render_template('about.html',
                           title='About',
                           is_about=True)


@app.route('/advice')
def advice():
    '''Advice Page'''
    return render_template('advice.html',
                           title='Advice')


@app.route('/creators')
def creators():
    '''Introduction Page about Us'''
    return render_template('creators.html',
                           title='Creators')


if __name__ == '__main__':
    app.run()
