#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#

from __future__ import absolute_import, unicode_literals

from datetime import datetime, date

from oclubs.access import database
from oclubs.enums import ActivityTime
from oclubs.objs.base import BaseObject, Property, ListProperty


def int_date(dateint):
    return datetime.strptime(str(dateint), Activity.date_fmtstr).date()


def date_int(dateobj):
    return int(dateobj.strftime(Activity.date_fmtstr))


class Activity(BaseObject):
    table = 'activity'
    identifier = 'act_id'
    name = Property('act_name')
    club = Property('act_club', 'Club')
    description = Property('act_desc', 'FormattedText')
    date = Property('act_date', (int_date, date_int))
    time = Property('act_time', ActivityTime)
    location = Property('act_location')
    cas = Property('act_cas')
    post = Property('act_post', 'FormattedText')
    attendance = ListProperty('attendance', 'att_act', 'att_user', 'User')
    pictures = ListProperty('act_pic', 'actpic_act', 'actpic_upload', 'Upload')

    date_fmtstr = '%Y%m%d'

    @property
    def ongoing_or_future(self):
        return self.datetime >= date.today()

    def signup(self, user, concentform=False):
        database.insert_or_update_row(
            'signup',
            {'signup_act': self.id, 'signup_user': user.id,
                'signup_consentform': concentform},
            {'signup_consentform': concentform}
        )

    def signup_undo(self, user):
        database.delete_rows(
            'signup',
            {'signup_act': self.id, 'signup_user': user.id}
        )

    def signup_list(self):
        from oclubs.objs import User

        ret = database.fetch_multirow(
            'signup',
            {'signup_act': self.id},
            {'signup_user': 'user', 'signup_consentform': 'consentform'}
        )
        for item in ret:
            item['user'] = User(item['user'])

        return ret

    def attend(self, user):
        database.insert_row(
            'attendance',
            {'att_act': self.id, 'att_user': user.id}
        )
        del self.attendance

    def attend_undo(self, user):
        database.delete_row(
            'attendance',
            {'att_act': self.id, 'att_user': user.id}
        )
        del self.attendance

    @classmethod
    def get_activities_conditions(cls, times=(), additional_conds=None,
                                  dates=(True, True), order_by_time=True,
                                  club_types=()):
        conds = {}
        if additional_conds:
            conds.update(additional_conds)

        conds['where'] = conds.get('where', [])
        if dates == (True, False):
            conds['where'].append(('<', 'act_date', date_int(date.today())))
        elif dates == (False, True):
            conds['where'].append(('>=', 'act_date', date_int(date.today())))

        if times:
            times = [time.value for time in times]
            conds['where'].append(('in', 'act_time', times))

        if club_types:
            club_types = [club_type.value for club_type in club_types]
            conds['join'] = conds.get('join', [])
            conds['join'].append(('inner', 'club', [('club_id', 'act_club')]))
            conds['where'].append(('in', 'club_type', club_types))

        if order_by_time:
            conds['order'] = conds.get('order', [])
            conds['order'].append(('act_date', True))

        acts = database.fetch_onecol(
            'activity',
            'act_id',
            conds
        )

        return [cls(act) for act in acts]

    @classmethod
    def all_activities(cls):
        return cls.get_activities_conditions()
