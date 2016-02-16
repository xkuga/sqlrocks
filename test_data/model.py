# -*- coding: utf-8 -*-

from test_data.config import *

to_obj = [
    {
        'data': None,
    },
    {
        'data': {'id': 1, 'name': 'Common Jasmin Orange'},
    },
    {
        'data': [
            {'id': 1, 'name': 'Common Jasmin Orange'},
            {'id': 2, 'name': 'Hair Like Snow'},
        ]
    },
]

select = [
    {
        'expr': 'id',
        'expected': 'SELECT id FROM %s' % table_song,
    },
    {
        'expr': ('id',),
        'expected': 'SELECT id FROM %s' % table_song,
    },
    {
        'expr': ['id', 'name'],
        'expected': 'SELECT id, name FROM %s' % table_song,
    },
]

get = [
    {
        'pk': 1,
        'expected': {
            'id': 1,
            'name': 'Common Jasmin Orange',
            'singer': 'Jay Chou',
            'tag': 'Incomparable',
            'is_published': 1,
        },
    },
    {
        'pk': 0,
        'expected': None,
    },
    {
        'pk': [1, 2],
        'expected': (
            {
                'id': 1,
                'name': 'Common Jasmin Orange',
                'singer': 'Jay Chou',
                'tag': 'Incomparable',
                'is_published': 1,
            },
            {
                'id': 2,
                'name': 'Hair Like Snow',
                'singer': 'Jay Chou',
                'tag': 'Chinese Style R&B',
                'is_published': 1,
            },
        ),
    },
]

one = [
    {
        'expr': '*',
        'where': 'id=1',
        'expected': {
            'id': 1,
            'name': 'Common Jasmin Orange',
            'singer': 'Jay Chou',
            'tag': 'Incomparable',
            'is_published': 1,
        },
    },
    {
        'expr': ['id', 'name'],
        'where': ('id', 1),
        'expected': {
            'id': 1,
            'name': 'Common Jasmin Orange',
        },
    },
    {
        'expr': ['id', 'name'],
        'where': ('id', 0),
        'expected': None,
    },
]

first = [
    {
        'expected': {
            'id': 1,
            'name': 'Common Jasmin Orange',
            'singer': 'Jay Chou',
            'tag': 'Incomparable',
            'is_published': 1,
        },
    }
]

last = [
    {
        'expected': {
            'id': 5,
            'name': 'You are Not Truly Happy',
            'singer': 'Mayday',
            'tag': '11752233',
            'is_published': 1,
        },
    }
]

exists = [
    {
        'where': 'id=0',
        'expected': False,
    },
    {
        'where': ('singer', 'kuga'),
        'expected': True,
    },
    {
        'where': [('singer', 'Jay Chou'), ('is_published', 1)],
        'expected': True,
    },
]

all = [
    {
        'expr': ['id', 'name'],
        'where': ('id', '<', 3),
        'order_by': 'id DESC',
        'limit': None,
        'expected': (
            {
                'id': 2,
                'name': 'Hair Like Snow',
            },
            {
                'id': 1,
                'name': 'Common Jasmin Orange',
            },
        ),
    },
    {
        'expr': ['id', 'name'],
        'where': ('id', '!=', 0),
        'order_by': 'id',
        'limit': (0, 2),
        'expected': (
            {
                'id': 1,
                'name': 'Common Jasmin Orange',
            },
            {
                'id': 2,
                'name': 'Hair Like Snow',
            },
        ),
    },
    {
        'expr': ['id', 'name'],
        'where': ('id', '=', 0),
        'order_by': 'id',
        'limit': [0, 2],
        'expected': (),
    },
]

count = [
    {
        'where': None,
        'expected': len(dataset[table_song]),
    },
    {
        'where': 'id=0',
        'expected': 0,
    },
    {
        'where': [('singer', 'Jay Chou'), ('is_published', 1)],
        'expected': 2,
    },
    {
        'where': {'OR': [('singer', 'Jay Chou'), ('singer', 'Mayday')]},
        'expected': 3,
    },
    {
        'where': ('singer', 'IN', ('Jay Chou', 'Mayday')),
        'expected': 3,
    },
]

add = [
    {
        'data': {'singer': 'Jay Chou'},
    },
    {
        'data': {'singer': 'Mayday'},
    },
]

saved = [
    {
        'data': {'singer': 'Jay Chou'},
        'insert': True,
    },
    {
        'data': {'id': 5, 'singer': 'Mayday', 'tag': 'band'},
        'insert': False,
    },
]

save = [
    {
        'data': {'singer': 'Jay Chou'},
        'insert': True,
    },
    {
        'data': {'id': 86, 'singer': 'kuga'},
        'insert': True,
    },
    {
        'data': {'id': 5},
        'modified': {'tag': 'rocks'}
    },
]

update = [
    {
        'data': {'singer': 'Jay Chou'},
        'where': ('id', 3),
    },
    {
        'data': {'singer': 'Mayday', 'tag': 'band'},
        'where': ('id', 3),
    },
]

delete = [
    {
        'where': ('id', 1),
        'affected_rows': 1,
    },
    {
        'where': ('singer', 'LIKE', '%ay%'),
        'affected_rows': 4,
    },
    {
        'where': None,
        'affected_rows': 5,
    },
    {
        'where': ('id', 0),
        'affected_rows': 0,
    },
]
