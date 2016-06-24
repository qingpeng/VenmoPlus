from flask import Flask
from flask import Flask,request, render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!"
@app.route('/realtime')
def realtime():
  return render_template("realtime.html")

