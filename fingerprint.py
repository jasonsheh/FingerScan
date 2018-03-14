#!/usr/bin/python
# __author__ = 'jasonsheh'
# -*- coding:utf-8 -*-

import sqlite3
import re
import requests


class FingerPrint:
    def __init__(self, url):
        self.conn = sqlite3.connect('Rules.db')
        self.cursor = self.conn.cursor()
        self.target = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}
        self.result = {}
        sql = 'select * from application'
        self.cursor.execute(sql)
        self.rules = self.cursor.fetchall()

    def init(self):
        if self.target.startswith('http://'):
            self.target = self.target[7:]
        elif self.target.startswith('https://'):
            self.target = self.target[8:]
        self.target = self.target.strip('/')

    def scan(self):
        finger_print = ''
        self.init()
        try:
            r = requests.get('http://' + self.target, timeout=2, headers=self.headers)
            for item in self.rules:
                appname = item[1]
                rules = item[2].split(', ')
                # print(app, rule)
                for rule in rules:
                    rule = rule.split(':', 1)
                    place = rule[0]
                    _rule = rule[1]
                    if place in ['body']:
                        if -1 != r.text.find(_rule):
                            finger_print += appname+' '
                            break
                    elif place in ['title']:
                        if re.search('<title>.*?'+re.escape(_rule)+'.*?</title>', r.text):
                            finger_print += appname+' '
                            break
                    elif place in ['header', 'server']:
                        header = ''
                        for key, value in r.headers.items():
                            header += key + ': ' + value + ' '
                        if re.search(re.escape(_rule), header, re.I):
                            finger_print += appname+' '
                            break
                    '''
                    elif place in ['fullheader', 'fullbody']:
                        if -1 != r.text.find(_rule):
                            finger_print += appname+' '
                            break
                        header = ''
                        for key, value in r.headers.items():
                            header += key + ': ' + value + ' '
                        if re.search(re.escape(_rule), header, re.I):
                            finger_print += appname+' '
                            break
                    '''
            self.result[self.target] = finger_print

        except requests.exceptions.ConnectionError:
            self.result[self.target] = ''
        except requests.exceptions.ReadTimeout:
            self.result[self.target] = ''
        except requests.exceptions.TooManyRedirects:
            self.result[self.target] = ''

    def run(self):
        self.scan()
        # Database().insert_finger(self.target, self.result[self.target])
        return self.result[self.target]


if __name__ == '__main__':
    url = input('请输入待识别域名: ')
    result = FingerPrint(url=url).run()
    print(result)
