# -*- coding: utf-8 -*-

import ddt
import json
import MySQLdb
import unittest

import test_data.sql
import test_data.db
import test_data.model
import test_data.config as config

from sqlrocks import *


class DbTestCase(unittest.TestCase):
    conn = None
    cur = None
    dataset = {}

    def setUp(self):
        self.conn = self.new_conn()

        if self.conn:
            self.cur = self.conn.cursor()
            self.create_dataset(self.conn, self.cur, self.get_dataset())

    def tearDown(self):
        if self.conn:
            self.delete_dataset(self.conn, self.cur, self.get_dataset())
            self.conn.close()

    @staticmethod
    def create_dataset(conn, cur, dataset):
        if conn and cur and dataset:
            for table, rows in dataset.items():
                for row in rows:
                    keys = row.keys()

                    keys_str = "`" + "`,`".join(keys) + "`"
                    placeholder = ("%s," * len(keys))[:-1]

                    if table and keys and placeholder:
                        sql = "INSERT INTO `%s` (%s) VALUES (%s)"
                        sql = sql % (table, keys_str, placeholder)
                        cur.execute(sql, row.values())

            conn.commit()

    @staticmethod
    def delete_dataset(conn, cur, dataset):
        if conn and cur and dataset:
            for table in dataset:
                DbTestCase.clear_table(conn, cur, table)

    @staticmethod
    def clear_table(conn, cur, table):
        cur.execute("TRUNCATE `%s`" % table)
        # cur.execute("DELETE FROM " + table)
        # cur.execute("ALTER TABLE " + table + " AUTO_INCREMENT = 1")

        conn.commit()

        return True

    def get_conn(self):
        if self.conn is None:
            self.conn = self.new_conn()
            if self.conn:
                self.cur = self.conn.cursor()
        return self.conn

    def get_cur(self):
        if self.cur is None:
            self.conn = self.new_conn()
            if self.conn:
                self.cur = self.conn.cursor()
        return self.cur

    def get_dataset(self):
        return self.dataset

    def new_conn(self):
        return self.conn


@ddt.ddt
class TestSql(unittest.TestCase):
    @ddt.data(*test_data.sql.parse_expr)
    @ddt.unpack
    def test_parse_expr(self, expr, expected):
        self.assertEqual(Sql.parse_expr(expr), expected)

    @ddt.data(*test_data.sql.parse_cond)
    @ddt.unpack
    def test_parse_cond(self, cond, expected):
        cond_str, cond_arg = Sql.parse_cond(cond)
        self.assertEqual(cond_str, expected['cond_str'])
        self.assertEqual(cond_arg, expected['cond_arg'])

    @ddt.data(*test_data.sql.flatten_where_cond)
    @ddt.unpack
    def test_flatten_where_cond(self, where, expected):
        cond_arg_list = []
        cond_str = Sql.flatten_where_cond(where, cond_arg_list)
        self.assertEqual(cond_str, expected['cond_str'])
        self.assertEqual(cond_arg_list, expected['cond_arg_list'])

    @ddt.data(*test_data.sql.parse_where_cond)
    @ddt.unpack
    def test_parse_where_cond(self, where, expected):
        cond_str, cond_arg_list = Sql.parse_where_cond(where)
        self.assertEqual(cond_str, expected['cond_str'])
        self.assertEqual(cond_arg_list, expected['cond_arg_list'])

    @ddt.data(*test_data.sql.select)
    @ddt.unpack
    def test_select(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.select(expr), Sql)
        self.assertEqual(sql.sql, expected['sql'])
        self.assertEqual(sql.args, expected['args'])

    @ddt.data(*test_data.sql.delete)
    @ddt.unpack
    def test_delete(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.delete(expr), Sql)
        self.assertEqual(sql.sql, expected['sql'])
        self.assertEqual(sql.args, expected['args'])

    @ddt.data(*test_data.sql.fr)
    @ddt.unpack
    def test_fr(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.fr(expr), Sql)
        self.assertEqual(sql.sql, expected['sql'])
        self.assertEqual(sql.args, expected['args'])

    @ddt.data(*test_data.sql.use_index)
    @ddt.unpack
    def test_use_index(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.use_index(expr), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.ignore_index)
    @ddt.unpack
    def test_ignore_index(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.ignore_index(expr), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.join)
    @ddt.unpack
    def test_join(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.join(expr), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.where_1)
    @ddt.unpack
    def test_where_1(self, condition, expected):
        sql = Sql()
        self.assertIsInstance(sql.where(condition), Sql)
        self.assertEqual(sql.sql, expected['cond_str'])
        self.assertEqual(sql.args, expected['cond_args'])

    @ddt.data(*test_data.sql.where_2)
    @ddt.unpack
    def test_where_2(self, condition, expected):
        sql = Sql()
        self.assertIsInstance(sql.where(**condition), Sql)
        self.assertIn(sql.sql, expected['cond_str_set'])
        self.assertIn(json.dumps(sql.args), expected['cond_args_set'])

    @ddt.data(*test_data.sql.group_by)
    @ddt.unpack
    def test_group_by(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.group_by(expr), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.having_1)
    @ddt.unpack
    def test_having_1(self, condition, expected):
        sql = Sql()
        self.assertIsInstance(sql.having(condition), Sql)
        self.assertEqual(sql.sql, expected['cond_str'])
        self.assertEqual(sql.args, expected['cond_args'])

    @ddt.data(*test_data.sql.having_2)
    @ddt.unpack
    def test_having_2(self, condition, expected):
        sql = Sql()
        self.assertIsInstance(sql.having(**condition), Sql)
        self.assertIn(sql.sql, expected['cond_str_set'])
        self.assertIn(json.dumps(sql.args), expected['cond_args_set'])

    @ddt.data(*test_data.sql.order_by)
    @ddt.unpack
    def test_order_by(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.order_by(expr), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.limit)
    @ddt.unpack
    def test_limit(self, args, expected):
        sql = Sql()
        self.assertIsInstance(sql.limit(*args), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.insert)
    @ddt.unpack
    def test_insert(self, table, expected):
        sql = Sql()
        self.assertIsInstance(sql.insert(table), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.update)
    @ddt.unpack
    def test_update(self, table, expected):
        sql = Sql()
        self.assertIsInstance(sql.update(table), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.sql_set)
    @ddt.unpack
    def test_set(self, expr, expected):
        sql = Sql()
        self.assertIsInstance(sql.set(expr), Sql)

        if isinstance(expr, dict):
            self.assertIn(sql.sql, expected['sql_set'])
            self.assertIn(json.dumps(sql.args), expected['args_set'])
        else:
            self.assertEqual(sql.sql, expected['sql'])
            self.assertEqual(sql.args, expected['args'])

    @ddt.data(*test_data.sql.alias)
    @ddt.unpack
    def test_alias(self, name, expected):
        sql = Sql()
        self.assertIsInstance(sql.alias(name), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.as_subquery)
    @ddt.unpack
    def test_as_subquery(self, alias, expected):
        sql = Sql()
        self.assertIsInstance(sql.as_subquery(alias), Sql)
        self.assertEqual(sql.sql, expected)

    @ddt.data(*test_data.sql.add_quote)
    @ddt.unpack
    def test_add_quote(self, expr, expected):
        sql = Sql()
        self.assertEqual(sql.add_quote(expr), expected)

    @ddt.data(*test_data.sql.chain)
    @ddt.unpack
    def test_query_chain(self, methods, expected):
        sql = Sql()

        for method in methods:
            getattr(sql, method['name'])(*method['args'])

        self.assertEqual(sql.sql, expected['sql'])
        self.assertEqual(sql.args, expected['args'])


@ddt.ddt
class TestDb(DbTestCase):
    db = None
    table = 'song'

    def setUp(self):
        self.db = self.new_test_db()
        self.conn = self.new_conn()
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.db.close()
        self.clear_table(self.conn, self.cur, self.table)
        self.conn.close()

    @ddt.data(*test_data.db.count)
    @ddt.unpack
    def test_count(self, dataset, where, expected):
        self.create_dataset(self.conn, self.cur, dataset)
        self.assertEqual(self.db.count(self.table, where), expected)

    @ddt.data(*test_data.db.insert)
    @ddt.unpack
    def test_insert(self, data):
        self.assertEqual(self.db.count(self.table), 0)

        insert_id = self.db.insert(self.table, data)
        self.db.commit()

        self.assertEqual(self.db.count(self.table), 1)

        sql = Sql().select(data.keys()).fr(self.table).where(id=insert_id)
        self.cur.execute(sql.val, sql.args)
        self.assertEqual(self.cur.fetchone(), data)

    @ddt.data(*test_data.db.update)
    @ddt.unpack
    def test_update(self, dataset, data, where):
        self.create_dataset(self.conn, self.cur, dataset)

        affected_rows = self.db.update(self.table, data, where)
        self.db.commit()

        self.assertEqual(affected_rows, 1)

        sql = Sql().select(data.keys()).fr(self.table).where(where)
        self.cur.execute(sql.val, sql.args)
        self.assertEqual(self.cur.fetchone(), data)

    @ddt.data(*test_data.db.save)
    @ddt.unpack
    def test_save(self, dataset, data, pk, insert):
        self.create_dataset(self.conn, self.cur, dataset)

        result = self.db.save(self.table, data, pk)
        self.db.commit()

        self.assertEqual(result, 1)
        pk_val = result if insert else data[pk]

        sql = Sql().select(data.keys()).fr(self.table).where(id=pk_val)
        self.cur.execute(sql.val, sql.args)
        self.assertEqual(self.cur.fetchone(), data)

    @ddt.data(*test_data.db.delete)
    @ddt.unpack
    def test_delete(self, dataset, where, affected_rows):
        self.create_dataset(self.conn, self.cur, dataset)
        self.assertEqual(self.db.count(self.table), len(dataset[self.table]))

        count = self.db.delete(self.table, where)

        self.assertEqual(count, affected_rows)
        self.assertEqual(self.db.count(self.table), 0)

    def new_test_db(self):
        conn = MySQLdb.connect(**config.db)
        return Db(conn, conn.cursor())

    def new_conn(self):
        return MySQLdb.connect(**config.db)


@ddt.ddt
class TestModel(DbTestCase):
    db = None
    model = None
    table = 'song'
    pk = 'id'

    def setUp(self):
        self.model = self.new_test_model()
        super(TestModel, self).setUp()

    def tearDown(self):
        self.model.db.close()
        super(TestModel, self).tearDown()

    @ddt.data(*test_data.model.to_obj)
    @ddt.unpack
    def test_to_obj(self, data):
        obj = self.model.to_obj(data)

        if data is None:
            self.assertEqual(obj, data)
        elif isinstance(data, dict):
            self.assertIsInstance(obj, self.model)
            self.assertEqual(obj._row, data)
        else:
            for i in range(len(data)):
                self.assertIsInstance(obj[i], self.model)
                self.assertEqual(obj[i]._row, data[i])

    @ddt.data(*test_data.model.select)
    @ddt.unpack
    def test_select(self, expr, expected):
        q = self.model.select(expr)

        self.assertIsInstance(q, Sql)
        self.assertEqual(q.sql, expected)

    @ddt.data(*test_data.model.get)
    @ddt.unpack
    def test_get(self, pk, expected):
        self.assertEqual(self.model.get(pk, fetch_obj=False), expected)

    @ddt.data(*test_data.model.one)
    @ddt.unpack
    def test_one(self, expr, where, expected):
        self.assertEqual(self.model.one(expr, where, fetch_obj=False), expected)

    @ddt.data(*test_data.model.first)
    @ddt.unpack
    def test_first(self, expected):
        self.assertEqual(self.model.first(fetch_obj=False), expected)

    @ddt.data(*test_data.model.last)
    @ddt.unpack
    def test_last(self, expected):
        self.assertEqual(self.model.last(fetch_obj=False), expected)

    @ddt.data(*test_data.model.exists)
    @ddt.unpack
    def test_exists(self, where, expected):
        self.assertEqual(self.model.exists(where), expected)

    @ddt.data(*test_data.model.all)
    @ddt.unpack
    def test_all(self, expr, where, order_by, limit, expected):
        actual = self.model.all(expr, where, order_by, limit, fetch_obj=False)
        self.assertEqual(actual, expected)

    @ddt.data(*test_data.model.count)
    @ddt.unpack
    def test_count(self, where, expected):
        self.assertEqual(self.model.count(where), expected)

    @ddt.data(*test_data.model.add)
    @ddt.unpack
    def test_add(self, data):
        pk = self.model.add(data)
        actual = self.model.get(pk, data.keys(), fetch_obj=False)
        self.assertEqual(actual, data)

    @ddt.data(*test_data.model.saved)
    @ddt.unpack
    def test_saved(self, data, insert):
        r = self.model.saved(data)

        if insert:
            pk = r
        else:
            self.assertEqual(r, 1)
            pk = data[self.model.pk]

        actual = self.model.get(pk, data.keys(), fetch_obj=False)
        self.assertEqual(actual, data)

    @ddt.data(*test_data.model.save)
    @ddt.unpack
    def test_save(self, data, insert=None, modified=None):
        obj = self.model(data)

        if modified:
            for k, v in modified.items():
                setattr(obj, k, v)

        r = obj.save(insert)

        if insert or self.model.pk not in data:
            pk = r
        else:
            self.assertEqual(r, 1)
            pk = data[self.model.pk]

        actual = self.model.get(pk, data.keys(), fetch_obj=False)
        self.assertEqual(actual, data)

    @ddt.data(*test_data.model.update)
    @ddt.unpack
    def test_update(self, data, where):
        affected_rows = self.model.update(data, where)
        self.assertEqual(affected_rows, 1)

        actual = self.model.one(data.keys(), where, fetch_obj=False)
        self.assertEqual(actual, data)

    @ddt.data(*test_data.model.delete)
    @ddt.unpack
    def test_delete(self, where, affected_rows):
        table_count = len(config.dataset[config.table_song])

        self.assertEqual(self.model.count(), table_count)
        self.assertEqual(self.model.delete(where), affected_rows)
        self.assertEqual(self.model.count(), table_count - affected_rows)

    @ddt.data(*test_data.model.remove)
    @ddt.unpack
    def test_remove(self, pk):
        total = self.model.count()
        obj = self.model.get(pk)

        self.assertEqual(obj.remove(), 1)
        self.assertEqual(self.model.count(), total - 1)

    def new_test_model(self):
        class Song(Model):
            table = self.table
            pk = self.pk
            db = self.new_test_db()

            @classmethod
            def get_fields(cls):
                return {'id', 'name', 'singer', 'tag', 'is_published'}

        return Song

    def new_test_db(self):
        conn = MySQLdb.connect(**config.db)
        return Db(conn, conn.cursor())

    def new_conn(self):
        return MySQLdb.connect(**config.db)

    def get_dataset(self):
        return config.dataset


if __name__ == '__main__':
    unittest.main()
