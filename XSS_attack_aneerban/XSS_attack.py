from flask import Flask,render_template,request, redirect, escape
from pathlib import Path
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from flask import make_response
import re
from datetime import datetime
import requests
from flask import escape
from bs4 import BeautifulSoup

app = Flask(__name__,template_folder='template')

@app.route('/reflected_xss_attack_form')
def reflected_xss_attack_form():
    return render_template('reflected_xss_attack_form.html')


@app.route('/reflected_xss_attack', methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
        form_data = request.form
        new_name= form_data["Name"]
        new_city= form_data["City"]
        new_country= form_data["Country"]
        r = make_response(render_template('data.html',name=new_name,city=new_city,country=new_country))
        return r


@app.route("/stored_xss_attack", methods=['POST', 'GET'])
def stored_xss_attack():

    data_base_file_name = "names.txt"

    if request.method == 'POST':
        name = request.form["name"]

        with open(data_base_file_name, "a") as f:
            f.write(name+"\n")

    names = ""
    with open(data_base_file_name, "r+") as f:
        for name in f.readlines():
            names+=name+"\n"

    r = make_response(render_template('stored_xss_form.html',Names=names))
    return r

@app.route("/dom_xss_attack")
#normal http://localhost:5010/dom_xss_attack?value=abs
#attack http://localhost:5010/dom_xss_attack?value=<script>alert("hi")</script>
def dom_xss_attack():
    value=request.args.get("value")
    print(value)
    r = make_response(render_template('dom_xss_form.html',value=value))
    return r



app.run(host='localhost', port=5010)
