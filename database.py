#!/usr/bin/python
# __author__ = 'jasonsheh'
# -*- coding:utf-8 -*-

import sqlite3


class Rules:
    def __init__(self):
        self.conn = sqlite3.connect('Rules.db')
        self.cursor = self.conn.cursor()

    def add_rule(self, name, rule):
        sql = "insert into application (name, rule) " \
              "values (?, ?)"
        self.cursor.execute(sql, (name, rule))
        self.conn.commit()
        self.clean()

    def delete_rule(self, name='', id=''):
        if id:
            sql = "delete from application where id = ?"
            self.cursor.execute(sql, (id,))
        else:
            sql = "delete from application where name = ?"
            self.cursor.execute(sql, (name, ))
        self.conn.commit()
        self.clean()

    def search_rule(self, name):
        sql = "select * from application where name like ?"
        self.cursor.execute(sql, ('%'+name+'%', ))
        results = self.cursor.fetchall()
        _results = []
        for result in results:
            _result = {}
            _result['id'] = result[0]
            _result['name'] = result[1]
            _result['rule'] = result[2]
            _results.append(_result)
        return _results

    def select_rule(self, page):
        sql = 'select * from application order by id desc limit ?,15'
        self.cursor.execute(sql, ((page-1)*15, ))
        results = self.cursor.fetchall()

        _results = []
        for result in results:
            _result = {}
            _result['id'] = result[0]
            _result['name'] = result[1]
            _result['rule'] = result[2]
            _results.append(_result)

        self.clean()
        return _results

    def count(self):
        self.cursor.execute('select count(*) from application')
        total = self.cursor.fetchone()
        return total[0]

    def clean(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    print(Rules().search_rule('nginx'))
