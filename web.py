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


@app.route('/search', methods=['POST'])
def add_task():
    if request.method == 'POST':
        if request.form.get('finger').find('.') != -1:
            result = FingerPrint(request.form.get('finger')).run()
            flash(result.split(' ')[:-1])
        return redirect('/index')


if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit()
