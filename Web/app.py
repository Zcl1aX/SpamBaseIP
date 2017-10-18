#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, url_for, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import fields, validators
from jinja2 import Environment
from werkzeug.contrib.fixers import ProxyFix
import redis

app = Flask(__name__)
Jinja2 = Environment()
app.config['SECRET_KEY'] = 'aGF*74(!fdaF3MlI2$2'

class SearchForm(FlaskForm):
    search_ip = fields.TextField('search', validators = [validators.Required()])



@app.route('/')
def home():
   return "Home"


@app.route('/search', methods = ['GET', 'POST'])
def search_ip():
    form = SearchForm()
    if form.validate_on_submit():

        pool = redis.StrictRedis(host='localhost', port=6379, db=0)
        s_ip = form.search_ip.data
        if '*' in s_ip:
            return ser_ip(s_ip)
        s_ip = "ip:"+s_ip
        req = list(pool.smembers(s_ip))

        if not req:
            error = s_ip + 'not found!'
            return render_template('error.html', title = 'Result', error=error)
        else:
            r = req[0].decode().replace(':', ' ')
            r = s_ip + r
            return render_template('oneip.html', title = 'Result', r=r)
    return render_template('sear.html', title = 'Search IP', form=form)


@app.route('/getip')
def getip():
    ip = request.args.get('ip', '')
    return ser_ip(ip)

def ser_ip(ip):
    pool = redis.StrictRedis(host='localhost', port=6379, db=0)
    s_ip = "ip:"+ip
    keys = pool.keys(s_ip)
    if not keys:
        error = s_ip + ' not found!'
        return render_template('error.html', title = 'Result', error=error)
    else:
        keys = [key.decode('utf-8') + ' ' + ip_info(key.decode('utf-8')) for key in keys]
        return render_template('bas.html', title = 'Search IP', keys=keys)




def ip_info(ip_):
    pool = redis.StrictRedis(host='localhost', port=6379, db=0)
    req = list(pool.smembers(ip_))
    if not req:
        out =  Jinja2.from_string(s_ip  + ' not found! ').render()
        return out
    else:
        out = req[0].decode().replace(':', ' ')
        return out

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.run()
