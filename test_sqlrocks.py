# -*- coding: utf-8 -*-

import re
import ddt
import unittest
import test_data.sql


from sqlrocks import *


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
            cols = re.findall(r'`(.+?)`=%s', expected['sql'])
            for i, col in enumerate(cols):
                self.assertEqual(expected['args'][i], expr[col])
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


if __name__ == '__main__':
    unittest.main()
