# -*- coding: utf-8 -*-

from test_data.config import *

count = [
    {
        'dataset': {
            table_song: []
        },
        'where': None,
        'expected': 0,
    },
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'secret', 'tag': ''},
                {'id': 2, 'name': 'abcdef', 'tag': ''},
            ]
        },
        'where': ('name', 'LIKE', '%abc%'),
        'expected': 1,
    },
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'secret', 'tag': ''},
                {'id': 2, 'name': 'abcdef', 'tag': ''},
            ]
        },
        'where': ('name', 'LIKE', '%null%'),
        'expected': 0,
    },
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'secret', 'tag': ''},
                {'id': 2, 'name': 'abcdef', 'tag': ''},
            ]
        },
        'where': None,
        'expected': 2,
    },
]

insert = [
    {
        'data': {'id': 1, 'name': 'Jay Chou'},
    },
    {
        'data': {'id': 1, 'name': 'Jay Chou'},
    },
]

update = [
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'Jay'},
            ]
        },
        'data': {'name': 'Jay Chou'},
        'where': ('id', 1),
    },
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'May', 'tag': ''},
            ]
        },
        'data': {'name': 'Mayday', 'tag': 'band'},
        'where': ('id', 1),
    },
]

save = [
    {
        'dataset': {},
        'data': {'name': 'Jay Chou'},
        'pk': 'id',
        'insert': True,
    },
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'May', 'tag': ''},
            ]
        },
        'data': {'id': 1, 'name': 'Mayday', 'tag': 'band'},
        'pk': 'id',
        'insert': False,
    },
]

delete = [
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'secret', 'tag': ''},
            ]
        },
        'where': ('id', 1),
        'affected_rows': 1,
    },
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'secret', 'tag': ''},
                {'id': 2, 'name': 'abcdef', 'tag': ''},
            ]
        },
        'where': ('name', 'LIKE', '%c%'),
        'affected_rows': 2,
    },
    {
        'dataset': {
            table_song: [
                {'id': 1, 'name': 'secret', 'tag': ''},
                {'id': 2, 'name': 'abcdef', 'tag': ''},
            ]
        },
        'where': None,
        'affected_rows': 2,
    },
]
