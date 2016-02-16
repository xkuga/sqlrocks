# -*- coding: utf-8 -*-

from sqlrocks import *

add_quote = [
    {
        'expr': ['id', 'name'],
        'expected': '`id`, `name`'
    },
    {
        'expr': ('id', 'name'),
        'expected': '`id`, `name`'
    },
    {
        'expr': 'id',
        'expected': '`id`'
    },
]

parse_expr = [
    {
        'expr': Sql('str', []),
        'expected': ('str', [])
    },
    {
        'expr': ('id',),
        'expected': ('id', [])
    },
    {
        'expr': ['id'],
        'expected': ('id', [])
    },
    {
        'expr': ['id', 'name'],
        'expected': ('id, name', [])
    },
    {
        'expr': ('id', 'name'),
        'expected': ('id, name', [])
    },
    {
        'expr': [Sql('str', [1])],
        'expected': ('str', [1])
    },
    {
        'expr': [Sql('foo', [1]), 'bar'],
        'expected': ('foo, bar', [1])
    },
    {
        'expr': ('bar', Sql('foo', [1])),
        'expected': ('bar, foo', [1])
    },
    {
        'expr': 'str',
        'expected': ('str', [])
    },
]

parse_cond = [
    {
        'cond': ['name IS NOT NULL'],
        'expected': {
            'cond_str': 'name IS NOT NULL',
            'cond_arg': None,
        },
    },
    {
        'cond': ('name', Sql('(subquery)', [5])),
        'expected': {
            'cond_str': 'name = (subquery)',
            'cond_arg': [5],
        },
    },
    {
        'cond': ['name', 'Jay Chou'],
        'expected': {
            'cond_str': 'name = %s',
            'cond_arg': 'Jay Chou',
        },
    },
    {
        'cond': ('year', 'BETWEEN', ('2010', '2014')),
        'expected': {
            'cond_str': 'year BETWEEN %s AND %s',
            'cond_arg': ('2010', '2014'),
        },
    },
    {
        'cond': ('year', 'BETWEEN', (2010, 2014)),
        'expected': {
            'cond_str': 'year BETWEEN %s AND %s',
            'cond_arg': (2010, 2014),
        },
    },
    {
        'cond': ('name', 'IN', Sql('(subquery)', [])),
        'expected': {
            'cond_str': 'name IN (subquery)',
            'cond_arg': [],
        },
    },
    {
        'cond': ('name', 'IN', {'Mayday'}),
        'expected': {
            'cond_str': 'name IN (%s)',
            'cond_arg': {'Mayday'},
        },
    },
    {
        'cond': ('name', 'IN', ['Jay Chou', 'Mayday']),
        'expected': {
            'cond_str': 'name IN (%s,%s)',
            'cond_arg': ['Jay Chou', 'Mayday'],
        },
    },
    {
        'cond': ('name', 'NOT IN', ('Jay Chou', 'Mayday')),
        'expected': {
            'cond_str': 'name NOT IN (%s,%s)',
            'cond_arg': ('Jay Chou', 'Mayday'),
        },
    },
    {
        'cond': ('name', '=', Sql('(subquery)', [5])),
        'expected': {
            'cond_str': 'name = (subquery)',
            'cond_arg': [5],
        },
    },
    {
        'cond': ('name', '=', 'Jay Chou'),
        'expected': {
            'cond_str': 'name = %s',
            'cond_arg': 'Jay Chou',
        },
    },
]

flatten_where_cond = [
    {
        'where': {
            'OR': [
                ('name', '=', 'Jay Chou'),
                {
                    'AND': [
                        ('name', 'LIKE', '%Mayday%'),
                        ('tag', '=', 'band'),
                    ]
                },
                ('id', '<', 5),
            ]
        },
        'expected': {
            'cond_str': '(name = %s OR (name LIKE %s AND tag = %s) OR id < %s)',
            'cond_arg_list': ['Jay Chou', '%Mayday%', 'band', 5],
        },
    },
    {
        'where': {
            'OR': [
                ('name', '=', 'Jay Chou'),
                {
                    'AND': (
                        'name != ""',
                        ('tag', '=', 'band'),
                    )
                },
                ('tag', '=', 'legend'),
            ]
        },
        'expected': {
            'cond_str': '(name = %s OR (name != "" AND tag = %s) OR tag = %s)',
            'cond_arg_list': ['Jay Chou', 'band', 'legend'],
        },
    },
    {
        'where': {
            'OR': [
                'name IS NOT NULL',
                'tag IS NOT NULL',
            ]
        },
        'expected': {
            'cond_str': '(name IS NOT NULL OR tag IS NOT NULL)',
            'cond_arg_list': [],
        },
    },
    {
        'where': {
            'AND': [
                ['name', '=', 'Jay Chou'],
            ]
        },
        'expected': {
            'cond_str': '(name = %s)',
            'cond_arg_list': ['Jay Chou'],
        },
    },
    {
        'where': {
            'AND': (
                ('name', '=', 'Mayday'),
            )
        },
        'expected': {
            'cond_str': '(name = %s)',
            'cond_arg_list': ['Mayday'],
        },
    },
    {
        'where': {
            'AND': [
                ['name', 'IN', {'Mayday'}],
                ['tag', '=', 'band']
            ]
        },
        'expected': {
            'cond_str': '(name IN (%s) AND tag = %s)',
            'cond_arg_list': ['Mayday', 'band'],
        },
    },
    {
        'where': {
            'AND': [
                ('name', '=', 'Mayday'),
                ('tag', '=', 'band'),
            ]
        },
        'expected': {
            'cond_str': '(name = %s AND tag = %s)',
            'cond_arg_list': ['Mayday', 'band'],
        },
    },
    {
        'where': {
            'AND': [
                ('name', 'IN', Sql('(subquery)', [1, 2])),
                ('tag', '=', 'legend'),
            ]
        },
        'expected': {
            'cond_str': '(name IN (subquery) AND tag = %s)',
            'cond_arg_list': [1, 2, 'legend'],
        },
    },
    {
        'where': {
            'AND': [
                ('name', Sql('(subquery)', [1, 2])),
                ('tag', '=', 'legend'),
            ]
        },
        'expected': {
            'cond_str': '(name = (subquery) AND tag = %s)',
            'cond_arg_list': [1, 2, 'legend'],
        },
    },
    {
        'where': {
            'AND': [
                ('name', '=', Sql('(subquery)', [1, 2])),
                'tag IS NOT NULL',
            ]
        },
        'expected': {
            'cond_str': '(name = (subquery) AND tag IS NOT NULL)',
            'cond_arg_list': [1, 2],
        },
    },
]

parse_where_cond = [
    {
        'where': None,
        'expected': {
            'cond_str': '',
            'cond_arg_list': None,
        }
    },
    {
        'where': 'str',
        'expected': {
            'cond_str': 'str',
            'cond_arg_list': None,
        }
    },
    {
        'where': ('name IS NOT NULL',),
        'expected': {
            'cond_str': '(name IS NOT NULL)',
            'cond_arg_list': [],
        },
    },
    {
        'where': ('name', '=', 'Jay Chou'),
        'expected': {
            'cond_str': '(name = %s)',
            'cond_arg_list': ['Jay Chou'],
        },
    },
    {
        'where': [
            ('name', '=', 'Jay Chou'),
        ],
        'expected': {
            'cond_str': '(name = %s)',
            'cond_arg_list': ['Jay Chou'],
        },
    },
    {
        'where': [
            ('name', '=', 'Jay Chou'),
            ('tag', '=', 'legend'),
        ],
        'expected': {
            'cond_str': '(name = %s AND tag = %s)',
            'cond_arg_list': ['Jay Chou', 'legend'],
        },
    },
    {
        'where': {
            'AND': (
                ('name', '=', 'Jay Chou'),
                ('tag', '=', 'legend'),
            )
        },
        'expected': {
            'cond_str': '(name = %s AND tag = %s)',
            'cond_arg_list': ['Jay Chou', 'legend'],
        },
    },
    {
        'where': [
            ('name', '=', 'Jay Chou'),
            ('tag IS NOT NULL',),
        ],
        'expected': {
            'cond_str': '(name = %s AND tag IS NOT NULL)',
            'cond_arg_list': ['Jay Chou'],
        },
    },
    {
        'where': [
            ('name', '=', 'Jay Chou'),
            'tag IS NOT NULL',
        ],
        'expected': {
            'cond_str': '(name = %s AND tag IS NOT NULL)',
            'cond_arg_list': ['Jay Chou'],
        },
    },
    {
        'where': [
            'name IS NOT NULL',
            'tag IS NOT NULL',
        ],
        'expected': {
            'cond_str': '(name IS NOT NULL AND tag IS NOT NULL)',
            'cond_arg_list': [],
        },
    },
]

select = [
    {
        'expr': 'id',
        'expected': {
            'sql': 'SELECT id',
            'args': [],
        },
    },
    {
        'expr': ('id', 'name'),
        'expected': {
            'sql': 'SELECT id, name',
            'args': [],
        },
    },
    {
        'expr': Sql('str', [5]),
        'expected': {
            'sql': 'SELECT str',
            'args': [5],
        },
    },
    {
        'expr': [Sql('str', [5]), 'name'],
        'expected': {
            'sql': 'SELECT str, name',
            'args': [5],
        },
    },
]

delete = [
    {
        'expr': None,
        'expected': {
            'sql': 'DELETE',
            'args': [],
        },
    },
    {
        'expr': ['t1'],
        'expected': {
            'sql': 'DELETE t1',
            'args': [],
        },
    },
    {
        'expr': ('t1', 't2'),
        'expected': {
            'sql': 'DELETE t1, t2',
            'args': [],
        },
    },
    {
        'expr': ('t1', Sql('str', [5])),
        'expected': {
            'sql': 'DELETE t1, str',
            'args': [5],
        },
    },
]

fr = [
    {
        'expr': 'song',
        'expected': {
            'sql': ' FROM song',
            'args': [],
        },
    },
    {
        'expr': ('song', 'singer'),
        'expected': {
            'sql': ' FROM song, singer',
            'args': [],
        },
    },
    {
        'expr': ['song', Sql('subquery', [5, 5])],
        'expected': {
            'sql': ' FROM song, subquery',
            'args': [5, 5],
        },
    },
]

use_index = [
    {
        'expr': 'str',
        'expected': ' USE INDEX(`str`)',
    },
    {
        'expr': ('id',),
        'expected': ' USE INDEX(`id`)',
    },
    {
        'expr': ['name', 'tag'],
        'expected': ' USE INDEX(`name`, `tag`)',
    },
]

ignore_index = [
    {
        'expr': 'str',
        'expected': ' IGNORE INDEX(`str`)',
    },
    {
        'expr': ('id',),
        'expected': ' IGNORE INDEX(`id`)',
    },
    {
        'expr': ['name', 'tag'],
        'expected': ' IGNORE INDEX(`name`, `tag`)',
    },
]

join = [
    {
        'expr': 'join string',
        'expected': ' join string',
    },
]

where_1 = [
    {
        'condition': 'id = 1',
        'expected': {
            'cond_str': ' WHERE id = 1',
            'cond_args': [],
        }
    },
    {
        'condition': ('id', 1),
        'expected': {
            'cond_str': ' WHERE (id = %s)',
            'cond_args': [1],
        }
    },
    {
        'condition': [('id', 1), ('name', 'Mayday')],
        'expected': {
            'cond_str': ' WHERE (id = %s AND name = %s)',
            'cond_args': [1, 'Mayday'],
        }
    },
]

where_2 = [
    {
        'condition': {'id': 1},
        'expected': {
            'cond_str': ' WHERE (id = %s)',
            'cond_args': [1],
        }
    },
    {
        'condition': {'id': 1, 'name': 'Mayday'},
        'expected': {
            'cond_str': ' WHERE (id = %s AND name = %s)',
            'cond_args': [1, 'Mayday'],
        }
    },
]

group_by = [
    {
        'expr': 'id',
        'expected': ' GROUP BY id',
    },
    {
        'expr': ('id', 'name'),
        'expected': ' GROUP BY id, name',
    },
]

having_1 = [
    {
        'condition': 'id = 1',
        'expected': {
            'cond_str': ' HAVING id = 1',
            'cond_args': [],
        }
    },
    {
        'condition': ('id', 1),
        'expected': {
            'cond_str': ' HAVING (id = %s)',
            'cond_args': [1],
        }
    },
    {
        'condition': [('id', 1), ('name', 'Mayday')],
        'expected': {
            'cond_str': ' HAVING (id = %s AND name = %s)',
            'cond_args': [1, 'Mayday'],
        }
    },
]

having_2 = [
    {
        'condition': {'id': 1},
        'expected': {
            'cond_str': ' HAVING (id = %s)',
            'cond_args': [1],
        }
    },
    {
        'condition': {'id': 1, 'name': 'Mayday'},
        'expected': {
            'cond_str': ' HAVING (id = %s AND name = %s)',
            'cond_args': [1, 'Mayday'],
        }
    },
]

order_by = [
    {
        'expr': None,
        'expected': '',
    },
    {
        'expr': 'id',
        'expected': ' ORDER BY id',
    },
    {
        'expr': ['id DESC', 'name ASC'],
        'expected': ' ORDER BY id DESC, name ASC',
    },
]

limit = [
    {
        'args': [None, None],
        'expected': '',
    },
    {
        'args': [[0, 5]],
        'expected': ' LIMIT 0, 5',
    },
    {
        'args': [(0, 5)],
        'expected': ' LIMIT 0, 5',
    },
    {
        'args': [5],
        'expected': ' LIMIT 5',
    },
    {
        'args': [0, 5],
        'expected': ' LIMIT 0, 5',
    },
    {
        'args': [5, 7],
        'expected': ' LIMIT 5, 7',
    },
]

insert = [
    {
        'table': 'song',
        'expected': 'INSERT INTO `song`',
    },
]

update = [
    {
        'table': 'song',
        'expected': 'UPDATE `song`',
    },
]

sql_set = [
    {
        'expr': {'name': 'Jay Chou'},
        'expected': {
            'sql': ' SET `name`=%s',
            'args': ['Jay Chou'],
        }
    },
    {
        'expr': {'name': 'Mayday', 'tag': 'band'},
        'expected': {
            'sql': ' SET `name`=%s, `tag`=%s',
            'args': ['Mayday', 'band'],
        }
    },
    {
        'expr': {'id': 5, 'name': 'Mayday', 'tag': 'band'},
        'expected': {
            'sql': ' SET `tag`=%s, `name`=%s, `id`=%s',
            'args': ['band', 'Mayday', 5],
        }
    },
    {
        'expr': 'str',
        'expected': {
            'sql': ' SET str',
            'args': [],
        }
    },
    {
        'expr': ['num=num+1', 'is_published=0'],
        'expected': {
            'sql': ' SET num=num+1, is_published=0',
            'args': []
        }
    },
]

alias = [
    {
        'name': 'foo',
        'expected': ' AS `foo`',
    },
]

as_subquery = [
    {
        'alias': 'foo',
        'expected': '() AS `foo`',
    },
]

chain = [
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'where',
                'args': [('name', 'Common Jasmin Orange')],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song WHERE (name = %s)',
            'args': ['Common Jasmin Orange'],
        }
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'use_index',
                'args': ['foo'],
            },
            {
                'name': 'where',
                'args': ['id != 0'],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song USE INDEX(`foo`) WHERE id != 0',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'ignore_index',
                'args': [('foo', 'bar')],
            },
            {
                'name': 'where',
                'args': ['id = 0'],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song IGNORE INDEX(`foo`, `bar`) WHERE id = 0',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'group_by',
                'args': ['tag'],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song GROUP BY tag',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'where',
                'args': ['id != 0'],
            },
            {
                'name': 'group_by',
                'args': ['tag'],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song WHERE id != 0 GROUP BY tag',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'group_by',
                'args': ['tag'],
            },
            {
                'name': 'having',
                'args': [('author', 'Jay Chou')],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song GROUP BY tag HAVING (author = %s)',
            'args': ['Jay Chou'],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'order_by',
                'args': [('id DESC', 'name ASC')],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song ORDER BY id DESC, name ASC',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'order_by',
                'args': ['id DESC'],
            },
            {
                'name': 'limit',
                'args': [5, 7],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song ORDER BY id DESC LIMIT 5, 7',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'insert',
                'args': ['song'],
            },
            {
                'name': 'set',
                'args': [{'name': 'Mayday'}],
            },
        ],
        'expected': {
            'sql': 'INSERT INTO `song` SET `name`=%s',
            'args': ['Mayday'],
        },
    },
    {
        'methods': [
            {
                'name': 'update',
                'args': ['song'],
            },
            {
                'name': 'set',
                'args': [{'name': 'Mayday'}],
            },
            {
                'name': 'limit',
                'args': [1],
            },
        ],
        'expected': {
            'sql': 'UPDATE `song` SET `name`=%s LIMIT 1',
            'args': ['Mayday'],
        },
    },
    {
        'methods': [
            {
                'name': 'delete',
                'args': [],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
        ],
        'expected': {
            'sql': 'DELETE FROM song',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'delete',
                'args': [],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'where',
                'args': [('id', '>', 1)],
            },
            {
                'name': 'order_by',
                'args': ['id'],
            },
            {
                'name': 'limit',
                'args': [1],
            },
        ],
        'expected': {
            'sql': 'DELETE FROM song WHERE (id > %s) ORDER BY id LIMIT 1',
            'args': [1],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'alias',
                'args': ['foo'],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song AS `foo`',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'as_subquery',
                'args': ['foo'],
            },
        ],
        'expected': {
            'sql': '(SELECT * FROM song) AS `foo`',
            'args': [],
        },
    },
    {
        'methods': [
            {
                'name': 'insert',
                'args': ['song'],
            },
            {
                'name': 'set',
                'args': [{'name': 'Mayday'}],
            },
        ],
        'expected': {
            'sql': 'INSERT INTO `song` SET `name`=%s',
            'args': ['Mayday'],
        },
    },
    {
        'methods': [
            {
                'name': 'update',
                'args': ['song'],
            },
            {
                'name': 'set',
                'args': [{'name': 'Mayday'}],
            },
            {
                'name': 'where',
                'args': [('id', 1)],
            },
        ],
        'expected': {
            'sql': 'UPDATE `song` SET `name`=%s WHERE (id = %s)',
            'args': ['Mayday', 1],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': [Sql('str', [5, 1]).as_subquery('foo')],
            },
            {
                'name': 'where',
                'args': [('id', 1)],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM (str) AS `foo` WHERE (id = %s)',
            'args': [5, 1, 1],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'where',
                'args': [('id', Sql('str', [5, 1]).as_subquery('foo'))],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song WHERE (id = (str) AS `foo`)',
            'args': [5, 1],
        },
    },
    {
        'methods': [
            {
                'name': 'select',
                'args': ['*'],
            },
            {
                'name': 'fr',
                'args': ['song'],
            },
            {
                'name': 'where',
                'args': [('id', 'IN', Sql('str', [5, 1]).as_subquery('foo'))],
            },
        ],
        'expected': {
            'sql': 'SELECT * FROM song WHERE (id IN (str) AS `foo`)',
            'args': [5, 1],
        },
    },
]
