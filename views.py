from flask import Flask, render_template, redirect, request, g, session, url_for, flash
# from model import User, Post
# from flask.ext.login import LoginManager, login_required, login_user, current_user
# from flaskext.markdown import Markdown
# import config
# import forms
import model
import json
import vote_funding_analysis

app = Flask(__name__)

@app.route("/")
# Displays a list of all current members of congress.
def index():
    legislator_list = model.get_all_current()
    return render_template('index.html', legislator_list=legislator_list)

@app.route("/member/<opensecrets_id>/contributions")
def table_sector_breakdown(opensecrets_id):
    # display sector contribution breakdown
    sector_total_dict = model.get_all_amounts(opensecrets_id)
    sector_keys = sector_total_dict.keys()
    sectors = model.get_sectors(opensecrets_id)
    legislator_data = model.get_legislator_name(opensecrets_id)

    return render_template('legislator.html', sectors=sectors, \
        opensecrets_id=opensecrets_id, sector_total_dict=sector_total_dict,\
        sector_keys=sector_keys, legislator=legislator_data[0], \
        district=legislator_data[1])


@app.route("/member/<opensecrets_id>/chart")
def make_bubbles(opensecrets_id):
    legislator_data = model.get_legislator_name(opensecrets_id)
    return render_template('bubble.html', opensecrets_id=opensecrets_id,\
        legislator=legislator_data[0], district=legislator_data[1])


@app.route("/member/<opensecrets_id>/contributions/json")
# An api request used by bubble.html to generate properly-formatted
# json for data from model.get_all_amounts
def view_sector_breakdown(opensecrets_id):
    sectors = model.make_json2(opensecrets_id)
    json_dump = json.dumps(sectors)
    return json_dump


@app.route('/test/json')
# An api request used by 
def create_json_test1():
    d = vote_funding_analysis.house_funding('h681-110.2008', 2006, 2008, 'F%')
    print d
    yea = d['Yea']
    nay = d['Nay']


    data = [{'name':'', 'children': yea}, {'name': '', 'children': nay}]
    data = json.dumps(data)

    return data

@app.route('/TARP')
def render2():
    return render_template('bubbles2.html')

if __name__ == "__main__":
    app.run(debug=True)
