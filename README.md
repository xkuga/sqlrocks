sqlrocks
========

A rockable SQL builder.

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

Tests
-----

Install requirements.

    pip install -r requirements.txt
    
Running test

    python test_sqlrocks.py

LICENSE
-------

MIT
