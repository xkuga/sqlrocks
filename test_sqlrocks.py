# -*- coding: utf-8 -*-

import re
import ddt
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
        self.create_dataset(self.get_conn(), self.get_dataset())

    def create_dataset(self, conn, dataset):
        if conn and dataset:
            cur = conn.cursor()

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

    def delete_dataset(self, conn, dataset):
        if conn and dataset:
            for table in dataset:
                self.clear_table(conn, table)

    def clear_table(self, conn, table):
        cur = conn.cursor()

        cur.execute("TRUNCATE `%s`" % table)
        # cur.execute("DELETE FROM " + table)
        # cur.execute("ALTER TABLE " + table + " AUTO_INCREMENT = 1")

        conn.commit()

        return True

    def get_conn(self):
        if self.conn is None:
            self.conn = self.create_conn()
            if self.conn:
                self.cur = self.conn.cursor()
        return self.conn

    def get_cur(self):
        if self.cur is None:
            self.conn = self.create_conn()
            if self.conn:
                self.cur = self.conn.cursor()
        return self.cur

    def get_dataset(self):
        return self.dataset

    def create_conn(self):
        return self.conn

    def tearDown(self):
        self.delete_dataset(self.get_conn(), self.get_dataset())


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
        self.assertEqual(sql.sql, expected['cond_str'])
        self.assertEqual(sql.args, expected['cond_args'])

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
        self.assertEqual(sql.sql, expected['cond_str'])
        self.assertEqual(sql.args, expected['cond_args'])

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
            cols = re.findall(r'`(.+?)`=%s', sql.sql)
            for i, col in enumerate(cols):
                self.assertEqual(sql.args[i], expr[col])
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
    @ddt.data(*test_data.db.count)
    @ddt.unpack
    def test_count(self, dataset, table, where, expected):
        db = self.get_test_db()

        try:
            self.create_dataset(self.conn, dataset)
            self.assertEqual(db.count(table, where), expected)
        finally:
            db.close()
            self.clear_table(self.conn, table)

    @ddt.data(*test_data.db.insert)
    @ddt.unpack
    def test_insert(self, table, data):
        db = self.get_test_db()

        try:
            self.assertEqual(db.count(table), 0)

            insert_id = db.insert(table, data)
            db.commit()

            self.assertEqual(db.count(table), 1)

            sql = "SELECT * FROM `%s` WHERE `id`='%s'" % (table, insert_id)
            self.cur.execute(sql)
            actual = self.cur.fetchone()

            for key in data:
                self.assertEqual(actual[key], data[key])
        finally:
            db.close()
            self.clear_table(self.conn, table)

    @ddt.data(*test_data.db.update)
    @ddt.unpack
    def test_update(self, dataset, table, data, where):
        db = self.get_test_db()

        try:
            self.create_dataset(self.conn, dataset)

            affected_rows = db.update(table, data, where)
            db.commit()

            self.assertEqual(affected_rows, 1)

            cond_str, cond_args = Sql.parse_where_cond(where)
            sql = "SELECT * FROM `%s` WHERE %s" % (table, cond_str)
            self.cur.execute(sql, cond_args)
            actual = self.cur.fetchone()

            for key in data:
                self.assertEqual(actual[key], data[key])
        finally:
            db.close()
            self.clear_table(self.conn, table)

    @ddt.data(*test_data.db.save)
    @ddt.unpack
    def test_save(self, dataset, table, data, pk, insert):
        db = self.get_test_db()

        try:
            self.create_dataset(self.conn, dataset)

            result = db.save(table, data, pk)
            db.commit()

            if insert:
                self.assertEqual(result, 1)
                pk_val = result
            else:
                self.assertEqual(result, 1)
                pk_val = data[pk]

            sql = "SELECT * FROM `%s` WHERE `%s`='%s'" % (table, pk, pk_val)
            self.cur.execute(sql)
            actual = self.cur.fetchone()

            for key in data:
                self.assertEqual(actual[key], data[key])
        finally:
            db.close()
            self.clear_table(self.conn, table)

    @ddt.data(*test_data.db.delete)
    @ddt.unpack
    def test_delete(self, dataset, table, where, affected_rows):
        db = self.get_test_db()

        try:
            self.create_dataset(self.conn, dataset)
            self.assertEqual(db.count(table), len(dataset[table]))

            count = db.delete(table, where)

            self.assertEqual(count, affected_rows)
            self.assertEqual(db.count(table), 0)
        finally:
            db.close()
            self.clear_table(self.conn, table)

    def get_test_db(self):
        conn = MySQLdb.connect(**config.db)
        return Db(conn, conn.cursor())

    def create_conn(self):
        return MySQLdb.connect(**config.db)


@ddt.ddt
class TestModel(DbTestCase):
    @ddt.data(*test_data.model.to_obj)
    @ddt.unpack
    def test_to_obj(self, data):
        model = self.get_test_model()
        obj = model.to_obj(data)

        if data is None:
            self.assertEqual(obj, data)
        elif isinstance(data, dict):
            self.assertIsInstance(obj, model)
            self.assertEqual(obj._row, data)
        else:
            for i in range(len(data)):
                self.assertIsInstance(obj[i], model)
                self.assertEqual(obj[i]._row, data[i])

    @ddt.data(*test_data.model.select)
    @ddt.unpack
    def test_select(self, expr, expected):
        model = self.get_test_model()
        q = model.select(expr)

        self.assertIsInstance(q, Sql)
        self.assertEqual(q.sql, expected)

    @ddt.data(*test_data.model.get)
    @ddt.unpack
    def test_get(self, pk, expected):
        model = self.get_test_model()

        try:
            self.assertEqual(model.get(pk, fetch_obj=False), expected)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.one)
    @ddt.unpack
    def test_one(self, expr, where, expected):
        model = self.get_test_model()

        try:
            actual = model.one(expr, where, fetch_obj=False)
            self.assertEqual(actual, expected)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.first)
    @ddt.unpack
    def test_first(self, expected):
        model = self.get_test_model()

        try:
            self.assertEqual(model.first(fetch_obj=False), expected)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.last)
    @ddt.unpack
    def test_last(self, expected):
        model = self.get_test_model()

        try:
            self.assertEqual(model.last(fetch_obj=False), expected)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.exists)
    @ddt.unpack
    def test_exists(self, where, expected):
        model = self.get_test_model()

        try:
            self.assertEqual(model.exists(where), expected)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.all)
    @ddt.unpack
    def test_all(self, expr, where, order_by, limit, expected):
        model = self.get_test_model()

        try:
            actual = model.all(expr, where, order_by, limit, fetch_obj=False)
            self.assertEqual(actual, expected)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.count)
    @ddt.unpack
    def test_count(self, where, expected):
        model = self.get_test_model()

        try:
            self.assertEqual(model.count(where), expected)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.add)
    @ddt.unpack
    def test_add(self, data):
        model = self.get_test_model()

        try:
            pk = model.add(data)
            actual = model.get(pk, data.keys(), fetch_obj=False)
            self.assertEqual(actual, data)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.saved)
    @ddt.unpack
    def test_saved(self, data, insert):
        model = self.get_test_model()

        try:
            r = model.saved(data)

            if insert:
                pk = r
            else:
                self.assertEqual(r, 1)
                pk = data[model.pk]

            actual = model.get(pk, data.keys(), fetch_obj=False)
            self.assertEqual(actual, data)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.save)
    @ddt.unpack
    def test_save(self, data, insert=None, modified=None):
        model = self.get_test_model()
        obj = model(data)

        try:
            if modified:
                for k, v in modified.items():
                    setattr(obj, k, v)

            r = obj.save(insert)

            if insert or model.pk not in data:
                pk = r
            else:
                self.assertEqual(r, 1)
                pk = data[model.pk]

            actual = model.get(pk, data.keys(), fetch_obj=False)
            self.assertEqual(actual, data)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.update)
    @ddt.unpack
    def test_update(self, data, where):
        model = self.get_test_model()

        try:
            affected_rows = model.update(data, where)

            self.assertEqual(affected_rows, 1)

            actual = model.one(data.keys(), where, fetch_obj=False)
            self.assertEqual(actual, data)
        finally:
            model.db.close()

    @ddt.data(*test_data.model.delete)
    @ddt.unpack
    def test_delete(self, where, affected_rows):
        model = self.get_test_model()

        try:
            table_count = len(config.dataset[config.table_song])
            self.assertEqual(model.count(), table_count)
            self.assertEqual(model.delete(where), affected_rows)
            self.assertEqual(model.count(), table_count - affected_rows)
        finally:
            model.db.close()

    def get_test_model(self):
        class Song(Model):
            table = 'song'
            pk = 'id'
            db = self.get_test_db()

            @classmethod
            def get_fields(cls):
                return {'id', 'name', 'singer', 'tag', 'is_published'}

        return Song

    def get_test_db(self):
        conn = MySQLdb.connect(**config.db)
        return Db(conn, conn.cursor())

    def create_conn(self):
        return MySQLdb.connect(**config.db)

    def get_dataset(self):
        return config.dataset


if __name__ == '__main__':
    unittest.main()
