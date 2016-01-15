# -*- coding: utf-8 -*-


class Sql:
    def __init__(self, sql='', args=None):
        """
        Init Sql instance

        :param str sql: sql string
        :param list args: sql arguments
        :return: Sql instance
        """
        self.sql = sql
        self.args = args if args else []

    @staticmethod
    def rocks():
        """
        MAYDAY ROCKS
        """
        print('\m/')

    @staticmethod
    def rockable():
        """
        TRUST ME
        """
        return True

    def select(self, expr='*'):
        """
        Select clause

        :param str|Sql|list|tuple expr: expression
        :return: Sql instance
        """
        expr, args = Sql.parse_expr(expr)

        self.sql += 'SELECT ' + expr
        self.args.extend(args)

        return self

    def delete(self, expr=None):
        """
        Delete clause

        :param list|tuple|str expr: expression
        :return: Sql instance
        """
        self.sql += 'DELETE'

        if expr:
            expr, args = Sql.parse_expr(expr)
            self.sql += ' ' + expr
            self.args.extend(args)

        return self

    def fr(self, expr):
        """
        From clause

        :param list|tuple|str expr: expression
        :return: Sql instance
        """
        expr, args = Sql.parse_expr(expr)

        self.sql += ' FROM ' + expr
        self.args.extend(args)

        return self

    def use_index(self, expr):
        """
        Use index clause

        :param list|tuple|str expr: expression
        :return: Sql instance
        """
        self.sql += ' USE INDEX(' + self.add_quote(expr) + ')'
        return self

    def ignore_index(self, expr):
        """
        Ignore index clause

        :param list|tuple|str expr: expression
        :return: Sql instance
        """
        self.sql += ' IGNORE INDEX(' + self.add_quote(expr) + ')'
        return self

    def join(self, expr):
        """
        From clause

        :param str expr: expression
        :return: Sql instance
        """
        self.sql += ' ' + expr
        return self

    def where(self, *args, **kwargs):
        """
        Where clause

        :param dict|list|tuple|str args: where conditions
        :return: Sql instance
        """
        cond = args[0] if args else kwargs.items()

        cond_str, cond_args = Sql.parse_where_cond(cond)

        if cond_str:
            self.sql += ' WHERE ' + cond_str
        if cond_args:
            self.args.extend(cond_args)

        return self

    def group_by(self, expr):
        """
        Group by clause

        :param list|tuple|str expr: expression
        :return: Sql instance
        """
        expr, args = Sql.parse_expr(expr)

        self.sql += ' GROUP BY ' + expr
        self.args.extend(args)

        return self

    def having(self, cond):
        """
        Having clause

        :param dict|list|tuple|str cond: where conditions
        :return: Sql instance
        """
        cond_str, cond_args = Sql.parse_where_cond(cond)

        if cond_str:
            self.sql += ' HAVING ' + cond_str
        if cond_args:
            self.args.extend(cond_args)

        return self

    def order_by(self, expr):
        """
        Order by clause

        :param list|tuple|str expr: expression
        :return: Sql instance
        """
        expr, args = Sql.parse_expr(expr)

        self.sql += ' ORDER BY ' + expr if expr else ''
        self.args.extend(args)

        return self

    def limit(self, a, b=None):
        """
        Limit clause

        :param int|str a: offset or length
        :param int|str b: length
        :return: Sql instance
        """
        if a is None and b is None:
            return self
        elif b is None:
            self.sql += ' LIMIT %s' % a
        elif a is None:
            self.sql += ' LIMIT %s' % b
        else:
            self.sql += ' LIMIT %s, %s' % (a, b)

        return self

    def insert(self, table):
        """
        Insert clause

        :param str table: table name
        :return: Sql instance
        """
        self.sql += 'INSERT INTO `%s`' % table
        return self

    def update(self, table):
        """
        Update clause

        :param str table: table name
        :return: Sql instance
        """
        self.sql += 'UPDATE `%s`' % table
        return self

    def set(self, expr):
        self.sql += ' SET '

        if isinstance(expr, dict):
            for k in expr:
                self.sql += '`' + k + '`=%s, '
                self.args.append(expr[k])
            self.sql = self.sql[0:-2]
        else:
            expr, args = Sql.parse_expr(expr)
            self.sql += expr
            self.args.extend(args)

        return self

    def alias(self, name):
        """
        Add alias

        :param name:
        :return: Sql Instance
        """
        self.sql += ' AS `%s`' % name
        return self

    def as_subquery(self, alias=None):
        """
        Set subquery

        :param str alias: subquery alias
        :return: Sql instance
        """
        if alias is None:
            self.sql = '(%s)' % self.sql
        else:
            self.sql = '(%s) AS `%s`' % (self.sql, alias)
        return self

    @staticmethod
    def add_quote(expr):
        """
        Add quote

        :param list|tuple|str expr:
        :return: string
        """
        if isinstance(expr, (list, tuple)):
            return '`' + '`, `'.join(expr) + '`'
        return '`' + expr + '`'

    @staticmethod
    def parse_expr(expr):
        """
        parse expression

        :param str|Sql|list|tuple expr: expression
        :return: expression string
        """
        if isinstance(expr, Sql):
            return expr.sql, expr.args
        elif isinstance(expr, (list, tuple)):
            str_list = []
            arg_list = []

            for i in expr:
                if isinstance(i, Sql):
                    arg_list.extend(i.args)
                    str_list.append(i.sql)
                else:
                    str_list.append(i)

            return ', '.join(str_list), arg_list
        else:
            return expr, []

    @staticmethod
    def parse_cond(v):
        """
        parse condition

        :param list|tuple v: condition details
        :return: condition string
        """
        cond_len = len(v)

        if cond_len == 1:
            return v[0], None
        elif cond_len == 2:
            if isinstance(v[1], Sql):
                return '%s = %s' % (v[0], v[1].sql), v[1].args
            else:
                return '%s = %s' % (v[0], '%s'), v[1]
        elif cond_len == 3:
            key = v[1].upper()

            if key == 'BETWEEN':
                return '%s %s %s' % (v[0], v[1], '%s AND %s'), v[2]
            elif key in {'IN', 'NOT IN'}:
                if isinstance(v[2], Sql):
                    return '%s %s %s' % (v[0], v[1], v[2].sql), v[2].args
                else:
                    placeholder = ('%s,' * len(v[2]))[:-1]
                    return '%s %s (%s)' % (v[0], v[1], placeholder), v[2]
            else:
                if isinstance(v[2], Sql):
                    return '%s %s %s' % (v[0], v[1], v[2].sql), v[2].args
                else:
                    return '%s %s %s' % (v[0], v[1], '%s'), v[2]

    @staticmethod
    def flatten_where_cond(where_cond, cond_arg_list):
        """
        flatten where conditions

        :param dict where_cond: where conditions
        :param list cond_arg_list: condition argument list
        :return: condition string
        """
        # get conjunction
        conj = list(where_cond.keys())[0]
        cond_str_list = []

        for val in where_cond[conj]:
            if isinstance(val, dict):
                cond_str_list.append(Sql.flatten_where_cond(val, cond_arg_list))
            elif isinstance(val, str):
                cond_str_list.append(val)
            else:
                cond_str, cond_arg = Sql.parse_cond(val)
                cond_str_list.append(cond_str)

                if cond_arg is not None:
                    if isinstance(cond_arg, (list, tuple, set)):
                        cond_arg_list.extend(cond_arg)
                    else:
                        cond_arg_list.append(cond_arg)

        conj = ' %s ' % conj

        return '(%s)' % conj.join(cond_str_list)

    @staticmethod
    def parse_where_cond(where_cond):
        """
        parse where conditions

        :param dict|list|tuple|str where_cond: where conditions
        :return: condition string
        """
        if where_cond is None:
            return '', None
        elif isinstance(where_cond, str):
            return where_cond, None
        else:
            # set default conjunction
            if not isinstance(where_cond, dict):
                if isinstance(where_cond, tuple):
                    where_cond = [where_cond]
                where_cond = {'AND': where_cond}

            cond_arg_list = []
            cond_str = Sql.flatten_where_cond(where_cond, cond_arg_list)

            return cond_str, cond_arg_list

    @property
    def val(self):
        return self.sql

    def __str__(self):
        return self.sql
