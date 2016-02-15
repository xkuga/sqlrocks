# -*- coding: utf-8 -*-

from MySQLdb.cursors import DictCursor

db = {
    'db': 'sqlrocks',
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '000000',
    'charset': 'utf8',
    'autocommit': False,
    'cursorclass': DictCursor,
}

table_song = 'song'

dataset = {
    table_song: [
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
        {
            'id': 3,
            'name': '',
            'singer': 'kuga',
            'tag': '',
            'is_published': 0,
        },
        {
            'id': 4,
            'name': 'Love Story',
            'singer': 'Taylor',
            'tag': 'Awesome',
            'is_published': 1,
        },
        {
            'id': 5,
            'name': 'You are Not Truly Happy',
            'singer': 'Mayday',
            'tag': '11752233',
            'is_published': 1,
        },
    ],
}
