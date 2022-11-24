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

def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")
def get_form_details(web_form):
    dict_details = {}
    dict_details["action"] = web_form.attrs.get("action", "").lower()
    dict_details["method"] = web_form.attrs.get("method", "").lower()
    inputs = []
    for form_tags in web_form.find_all("input"):
        _type = form_tags.attrs.get("type", "text")
        _name = form_tags.attrs.get("name")
        inputs.append({"type": _type, "name": _name})
    dict_details["inputs"] = inputs
    return dict_details
def final_form(form_details, url, value):
    final_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    _data = {}
    for i in inputs:
        if i["type"] == "text" or i["type"] == "search":
            i["value"] = value
        _name = i.get("name")
        _value = i.get("value")
        if _name and _value:
            _data[_name] = _value
    return requests.post(final_url, data=_data)
@app.route('/')
def basefn():
    return "Hello"

@app.route('/dom_attack_form')
def reflected_xss_attack_form():
    resp = make_response(render_template('dom_attack_form.html'))
    resp.set_cookie("cookie", "secret")
    return resp

@app.route('/dom_defense_form')
def reflected_xss_defense_form():
    return render_template('dom_defense_form.html')

@app.route('/dom_attack', methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
        form_data = request.form
        new_name= form_data["Name"]
        new_city= form_data["City"]
        new_country= form_data["Country"]
        r = make_response(render_template('data.html',name=new_name,city=new_city,country=new_country))
        return r

@app.route('/dom_defense', methods = ['POST', 'GET'])
def data_protection():
    if request.method == 'POST':
        form_data = request.form
        new_name= re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', form_data["Name"])
        new_city= re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', form_data["City"])
        new_country= re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', form_data["Country"])
        r = make_response(render_template('data.html',name=new_name,city=new_city,country=new_country))
        r.headers.set('Content-Security-Policy', "script-src 'none'")
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

@app.route("/stored_xss_defense", methods=['POST', 'GET'])
def stored_xss_defense():

    data_base_file_name = "names.txt"

    if request.method == 'POST':
        name = request.form["name"]
        print(escape(name))

        with open(data_base_file_name, "a") as f:
            f.write(escape(name)+"\n")

    names = ""
    with open(data_base_file_name, "r+") as f:
        for name in f.readlines():
            names+=name+"\n"

    r = make_response(render_template('stored_xss_form.html',Names=names))
    r.headers.set('Content-Security-Policy', "script-src 'none'")
    return r

@app.route("/reflected_xss_attack")
#normal http://localhost/reflected_xss_attack?value=abs
#attack http://localhost/reflected_xss_attack?value=<script>alert("hi")</script>
def dom_xss_attack():
    value=request.args.get("value")
    print(value)
    r = make_response(render_template('reflected_xss.html',value=value))
    return r

@app.route("/reflected_xss_defense")
#http://localhost/reflected_xss_defense?value=<script>alert("hi")</script>
def dom_xss_defense():
    to_clean = re.compile('<.*?>')
    value=request.args.get("value")
    cleantext = re.sub(to_clean, '', value)
    cleaned_value=cleantext
    print(cleaned_value)
    r = make_response(render_template('reflected_xss.html',value=cleaned_value))
    r.headers.set('Content-Security-Policy', "script-src 'none'")
    return r

    #return page
def form_analysis(forms,url):
    js_script = "<script>alert('bye')</script>"
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = final_form(form_details, url, js_script).content.decode()
        if js_script in content:
            is_vulnerable = True
    return {"vulneribility_detected":is_vulnerable}

@app.route('/validate_xss_attack_forms', methods = ['POST', 'GET'])
def scan_attack_form():
    url="http://localhost/dom_attack_form"
    forms = get_all_forms(url)
    _validation_dict=form_analysis(forms,url)
    return _validation_dict

@app.route('/validate_xss_defense_forms', methods = ['POST', 'GET'])
def scan_defense_form():
    url="http://localhost/dom_defense_form"
    forms = get_all_forms(url)
    _validation_dict=form_analysis(forms,url)
    return _validation_dict



app.run(host='0.0.0.0', port=80)
