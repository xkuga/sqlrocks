sqlrocks
========

A rockable SQL builder with a lightweight ORM. \m/

Rock Start
----------

```python
>>> from sqlrocks import *
>>> Sql().select().fr('singer').val
'SELECT * FROM singer'
>>> sql = Sql().select().fr('singer').where(name='Mayday')
>>> sql.val
'SELECT * FROM singer WHERE (name = %s)'
>>> sql.args
['Mayday']
>>> sql = Sql().select().fr('singer').where(('id', 'IN', {1, 2}))
>>> sql.val
'SELECT * FROM singer WHERE (id IN (%s,%s))'
>>> sql.args
[1, 2]
>>> sql = Sql().insert('singer').set({'id': 1, 'name': 'Jay Chou'})
>>> sql.val
'INSERT INTO `singer` SET `name`=%s, `id`=%s'
>>> sql.args
['Jay Chou', 1]
>>> sql = Sql().update('singer').set({'name': 'Jay Chou'}).where(id=1)
>>> sql.val
'UPDATE `singer` SET `name`=%s WHERE (id = %s)'
>>> sql.args
['Jay Chou', 1]
```

Where Condition
---------------

More examples about where condition.

```python
# u can drop the '='
where = ('name', '=', 'Mayday')
where = ('name', 'Mayday')

# u can drop the 'AND'
where = {
    'AND': [
        ['name', 'Jay Chou'],
        ['tag', 'legend'],
    ]
}
where = [('name', 'Jay Chou'), ('tag', 'legend')]

# complicated where condition
where =  {
    'OR': (
        ('name', '=', 'Mayday'),
        {
            'AND': (
                ('name' '=', 'Jay Chou'),
                ('tag', '=', 'legend'),
            )
        },
    )
}
```

**Use tuple for one argument, list for multiple arguments.**

```python
where = ('name', '=', 'Mayday') # ok~
where = ['name', '=', 'Mayday'] # wrong!

where = [('name', '=', 'Mayday'), ('tag', '=', 'band')] # ok~
where = [['name', '=', 'Mayday'], ['tag', '=', 'band']] # ok~
where = (('name', '=', 'Mayday'), ('tag', '=', 'band')) # wrong!
```

ORM
===

Create MySQLdb connection and model class:

```python
import MySQLdb

from sqlrocks import *
from MySQLdb.cursors import DictCursor

conn = MySQLdb.connect(
    db='music',
    host='127.0.0.1',
    port=3306,
    user='user',
    passwd='passwd',
    charset='utf8',
    autocommit=True,
    cursorclass=DictCursor,
)

db = Db(conn, conn.cursor())

class Singer(Model):
    table = 'singer'
    pk = 'id'
    db = db
    
    @classmethod
    def get_fields(cls):
        return ['id', 'name', 'tag']
```

Basic usage:

```python
>>> Singer.add(name='Mayday')
1
>>> Singer(name='instance').save()
2
>>> Singer.saved({'name': 'Jay Chou'})
3
>>> Singer.count()
3
>>> Singer.first().name
'Mayday'
>>> Singer.last().name
'Jay Chou'
>>> Singer.get(2).name
'instance'
>>> Singer.get([1, 3])[0].name
'Mayday'
>>> Singer.one(expr=['id', 'name'], where=('id', 3)).name
'Jay Chou'
>>> Singer.all(order_by='-id')[0].name
'Jay Chou'
>>> Singer.all(order_by='id', limit=1, fetch_obj=False)
({'name': 'Mayday', 'tag': '', 'id': 1},)
>>> mayday = Singer.get(1)
>>> mayday.tag = 'rocks'
>>> mayday.save()
1
>>> Singer.get(1).tag
'rocks'
>>> Singer.update({'tag': 'Incomparable'}, where=('name', 'Jay Chou'))
1
>>> Singer.get(3).tag
'Incomparable'
>>> Singer.saved({'id': 2, 'tag': 'XD'})
1
>>> instance = Singer.get(2)
>>> instance.tag
'XD'
>>> instance['tag']
'XD'
>>> instance.remove()
1
>>> Singer.count()
2
>>> Singer.delete()
2
>>> Singer.count()
0
```

Traversing foreign key does not support. It's not free.

Installation
------------

    $ pip install sqlrocks

Tests
-----

Install requirements.

    $ pip install -r requirements.txt
    
Running test

    $ python test_sqlrocks.py

LICENSE
-------

MIT
