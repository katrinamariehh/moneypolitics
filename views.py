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
# app.config.from_object(config)

@app.route("/member/<opensecrets_id>/chart")
def make_bubbles(opensecrets_id):
    json_dump = json.dumps(model.make_json(opensecrets_id))
    return render_template('bubble.html', opensecrets_id=opensecrets_id)

@app.route("/")
def index():
    # display all legislators
    legislator_list = model.get_all_current()
    return render_template('index.html', legislator_list=legislator_list)

@app.route("/member/<opensecrets_id>/contributions")
def table_sector_breakdown(opensecrets_id):
    # display sector contribution breakdown
    sector_total_dict = model.get_all_amounts(opensecrets_id)
    sectors = model.get_sectors(opensecrets_id)
    return render_template('legislator.html', sectors=sectors, \
        opensecrets_id=opensecrets_id, sector_total_dict=sector_total_dict)

@app.route("/member/<opensecrets_id>/contributions/json")
# an api request used by bubble.html to generate properly-formatted json
# for data from model.get_all_amounts
def view_sector_breakdown(opensecrets_id):
    sectors = model.make_json2(opensecrets_id)
    json_dump = json.dumps(sectors)
    return json_dump

@app.route("/member/<member_id>/votes")
def view_vote_breakdown(member_id):
    # display votes by subject of bill
    return render_template('template_name')

@app.route('/test/json')
def create_json_test1():
    d = vote_funding_analysis.house_funding('h681-110.2008', 2006, 2008, 'F%')
    print d
    yea = d['Yea']
    nay = d['Nay']


    data = [{'name':'', 'children': yea}, {'name': '', 'children': nay}]
    data = json.dumps(data)


    # need to add names in here somewhere and a color
    return data

@app.route('/test/json2')
def create_json_test2():
    # d = vote_funding_analysis.house_funding('h681-110.2008', 2006, 2008, 'F%')
    # yea = d['Yea']
    # # j = json.dumps(yea)
    # nay = d['Nay']

    # list_of_dicts = [{'name': 'Yea', 'size': yea}, {'name': 'Nay', 'size': nay}

    # list_of_dicts = [{"color": "rgb(0,89,50)", "name": "Agribusiness", "size": 40550}, {"color": "rgb(0,89,28)", "name": "Defense", "size": 23500}, {"color": "rgb(0,89,121)", "name": "Transportation", "size": 98550}, {"color": "rgb(0,89,1)", "name": "Non-contribution", "size": 1500}, {"color": "rgb(0,89,216)", "name": "Lawyers & Lobbyists", "size": 175355}, {"color": "rgb(0,89,357)", "name": "Finance/Insur/RealEst", "size": 289825}, {"color": "rgb(0,89,423)", "name": "Misc Business", "size": 343171}, {"color": "rgb(0,89,113)", "name": "Communic/Electronics", "size": 91950}, {"color": "rgb(0,89,573)", "name": "Energy/Nat Resource", "size": 465383}, {"color": "rgb(0,89,472)", "name": "Ideology/Single-Issue", "size": 383561}, {"color": "rgb(0,89,104)", "name": "Other", "size": 84708}, {"color": "rgb(0,89,582)", "name": "Health", "size": 472433}, {"color": "rgb(0,89,265)", "name": "Construction", "size": 215148}, {"color": "rgb(0,89,480)", "name": "Unknown", "size": 389783}, {"color": "rgb(0,89,181)", "name": "Labor", "size": 147085}]

    list_of_dicts = [
                    {
                     "name": "", 
                      "children": [
                        {"name": "One", "size": 1000},
                        {"name": "Two", "size": 2000},
                        {"name": "Three", "size": 3000},
                        {"name": "Four", "size": 4000}
                      ]
                    },
                     {
                      "name": "", 
                       "children": [
                        {"name": "One", "size": 1000},
                        {"name": "Two", "size": 2000},
                        {"name": "Three", 'size': 3000},
                        {'name': 'Four', 'size': 4000}
                      ]
                    }
                    ]
    
    data = json.dumps(list_of_dicts)


    # need to add names in here somewhere and a color
    return data
    return list_of_dicts

@app.route('/test')
def render2():
    return render_template('bubbles2.html')

@app.route('/test2')
def render3():
    return render_template('bubbles3.html')


if __name__ == "__main__":
    app.run(debug=True)
