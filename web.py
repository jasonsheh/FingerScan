#!/usr/bin/python
# __author__ = 'jasonsheh'
# -*- coding:utf-8 -*-

import sys
from fingerprint import FingerPrint
from database import Rules
from flask import Flask, render_template, request, redirect, flash


app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
@app.route('/index')
def index():
    total_number = Rules().count()
    return render_template('index.html', total_number=total_number)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') and request.form.get('password'):
            username = request.form.get('username')
            password = request.form.get('password')

            if username == 'admin' and password == 'password':
                return render_template('manage.html')
        return redirect('/index')


@app.route('/fingerprint', methods=['POST'])
def add_task():
    if request.method == 'POST':
        if request.form.get('finger').find('.') != -1:
            result = FingerPrint(request.form.get('finger')).run()
            flash(result.split(' ')[:-1])
        return redirect('/index')


@app.route('/add', methods=['POST'])
def add_rule():
    if request.method == 'POST':
        if request.form.get('name') and request.form.get('rule'):
            name = request.form.get('name')
            rule = request.form.get('rule')
            Rules().add_rule(name, rule)
        return render_template('manage.html')


@app.route('/delete', methods=['POST'])
def delete_rule():
    if request.method == 'POST':
        if request.form.get('name'):
            name = request.form.get('name')
            Rules().delete_rule(name=name)
        if request.form.get('id'):
            id = request.form.get('id')
            Rules().delete_rule(id=id)
        return render_template('manage.html')


@app.route('/search', methods=['POST'])
def search_rule():
    if request.method == 'POST':
        if request.form.get('name'):
            name = request.form.get('name')
            results = Rules().search_rule(name)
            return render_template('manage.html', results=results)


if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit()
