#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#

from flask import (
    Blueprint, render_template, url_for
)

import traceback

clubblueprint = Blueprint('clubblueprint', __name__)


@clubblueprint.route('/clublist')
def clublist():
    '''Club List'''
    user = ''
    clubs = [{'name': 'Art Club', 'photo': 'intro1', 'intro': 'Here is where birth of arts happens'},
             {'name': 'Photo Club', 'photo': 'intro2', 'intro': 'Place for photography!'},
             {'name': 'Art Club', 'photo': 'intro3', 'intro': 'Here is where birth of arts happens'},
             {'name': 'Photo Club', 'photo': 'intro3', 'intro': 'Place for photography!'},
             {'name': 'Art Club', 'photo': 'intro4', 'intro': 'Here is where birth of arts happens'},
             {'name': 'Photo Club', 'photo': 'intro5', 'intro': 'Place for photography!'},
             {'name': 'Art Club', 'photo': 'intro6', 'intro': 'Here is where birth of arts happens'},
             {'name': 'Photo Club', 'photo': 'intro7', 'intro': 'Place for photography!'},
             {'name': 'Art Club', 'photo': 'intro8', 'intro': 'Here is where birth of arts happens'},
             {'name': 'Photo Club', 'photo': 'intro9', 'intro': 'Place for photography!'}]
    return render_template('clublist.html',
                           title='Club List',
                           is_list=True,
                           user=user,
                           clubs=clubs)


@clubblueprint.route('/clubintro')
def clubintro():
    '''Club Intro'''
    user = ''
    intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    return render_template('clubintro.html',
                           title='Club Intro',
                           user=user,
                           intro=intro)


@clubblueprint.route('/newleader')
def newleader():
    '''Selecting New Club Leader'''
    user = ''
    leader = {'official_name': 'Feng Ma', 'nick_name': 'Principal Ma', 'photo': '4'}
    members = [{'official_name': 'Ichiro Tai', 'nick_name': 'Derril', 'photo': '1'},
               {'official_name': 'YiFei Zhu', 'nick_name': 'YiFei', 'photo': '2'},
               {'official_name': 'Frank Lee', 'nick_name': 'Frank', 'photo': '3'},
               {'official_name': 'Ichiro Tai', 'nick_name': 'Derril', 'photo': '1'},
               {'official_name': 'YiFei Zhu', 'nick_name': 'YiFei', 'photo': '2'},
               {'official_name': 'Frank Lee', 'nick_name': 'Frank', 'photo': '3'},
               {'official_name': 'Ichiro Tai', 'nick_name': 'Derril', 'photo': '1'},
               {'official_name': 'YiFei Zhu', 'nick_name': 'YiFei', 'photo': '2'},
               {'official_name': 'Frank Lee', 'nick_name': 'Frank', 'photo': '3'},
               {'official_name': 'Ichiro Tai', 'nick_name': 'Derril', 'photo': '1'},
               {'official_name': 'YiFei Zhu', 'nick_name': 'YiFei', 'photo': '2'},
               {'official_name': 'Frank Lee', 'nick_name': 'Frank', 'photo': '3'},
               {'official_name': 'Ichiro Tai', 'nick_name': 'Derril', 'photo': '1'},
               {'official_name': 'YiFei Zhu', 'nick_name': 'YiFei', 'photo': '2'},
               {'official_name': 'Frank Lee', 'nick_name': 'Frank', 'photo': '3'}]
    return render_template('newleader.html',
                           title='New Leader',
                           user=user,
                           leader=leader,
                           members=members)


@clubblueprint.route('/club')
def clubmanage():
    '''Club Management Page'''
    user = ''
    club = 'Website Club'
    return render_template('club.html',
                           title=club,
                           user=user,
                           club=club)