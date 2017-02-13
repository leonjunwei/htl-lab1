"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""
import os
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

courses = pd.read_csv('./data/olin-courses-16-17.csv')


def flip(name): #turns A, B into B, A. It also needs to turn A, B ; C, D into B A; D C
    return " ".join(name.split(", ")[::-1])

def parse(names):
    if ";" in names:
        return "; ".join([flip(name) for name in names.split("; ")])
    else:
        return flip(names)

# print(flip('Dabby, Diana'))
# print parse("Lynch, Caitrin; Ben-Ur, Ela")


@app.route('/health')
def health():
    return 'ok'

@app.route('/')
def home_page():
    return render_template('index.html', areas=set(courses.course_area), contacts=set(parse(name) for name in set(courses.course_contact.dropna())))

@app.route('/area/<course_area>')
def area_page(course_area):
    return render_template('course_area.html', courses=courses[courses.course_area == course_area].iterrows())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    environment = os.environ.get('ENVIRONMENT',None)
    if environment:
        app.run(host='0.0.0.0', debug=True, port=port)
    else:
        app.run(host='127.0.0.1', debug=True, port=port)
