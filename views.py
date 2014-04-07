from flask import Flask, render_template, redirect, request, g, session, url_for, flash
# from model import User, Post
# from flask.ext.login import LoginManager, login_required, login_user, current_user
# from flaskext.markdown import Markdown
# import config
# import forms
import model
import json
import vote_funding_analysis
import locale

app = Flask(__name__)

locale.setlocale(locale.LC_ALL, '')

@app.route("/")
# Displays a list of all current members of congress.
def index():
    data = model.get_all_current()
    legislator_list = data[0]
    senators = data[1]
    representatives = data[2]
    return render_template('index.html', legislator_list=legislator_list,\
        senators=senators, representatives=representatives)

@app.route("/member/<opensecrets_id>/contributions")
# display sector contribution breakdown
def table_sector_breakdown(opensecrets_id):

    sector_total_dict = model.get_all_amounts(opensecrets_id)
    keys2 = sector_total_dict.keys()

    for key in keys2:
        sector_total_dict[key] = locale.currency(sector_total_dict[key], \
            grouping=True)

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


@app.route('/TARP/json')
def create_json_tarp():
    """An api request used by tarp.html to render bubble graph of
    financial sector contributions to members of congress in 2006 and
    2008 and how they voted on this particular bill; each bubble's
    radius is determined by the size of the donation and donations
    are grouped by vote value (Yea or Nay).

    The code that is commented out runs the actual request which needs
    to be optimized; its output has been saved to tarp.json to allow
    the page to load easily for the time being.
    """
    # d = vote_funding_analysis.house_funding('h681-110.2008', 2006, 2008, 'F%')

    # yea = d['Yea']
    # nay = d['Nay']


    # data = [{'name':'Yea', 'children': yea, 'color': '#1F8A70'},\
    # {'name': 'Nay', 'children': nay, 'color': '#BEDB39'}]
    # data = json.dumps(data)

    # return data
    json_data = open('tarp.json')
    data = json.load(json_data)
    data2 = json.dumps(data)
    return data2


@app.route('/TARP')
def render2():
    return render_template('tarp.html')

@app.route('/PPACA/json')
def create_json_ppaca():
    """An api request used by ppaca.html to render bubble graph of
    health sector contributions to members of congress in 2008 and
    2010 and how they voted on this particular bill; each bubble's
    radius is determined by the size of the donation and donations
    are grouped by vote value (Yea or Nay).

    The code that is commented out runs the actual request which needs
    to be optimized; its output has been saved to ppaca.json to allow
    the page to load easily for the time being.
    """
    # d = vote_funding_analysis.house_funding('h165-111.2010', 2008, 2010, 'H%')

    # aye = d['Aye']
    # no = d['No']

    # ppaca_votes = [{'name': 'Aye', 'children': aye, 'color': '#1F8A70', 'opacity': '100'},\
    # {'name': 'No', 'children': no, 'color': '#BEDB39', 'opacity': '100'}]
    # ppaca_votes = json.dumps(ppaca_votes)

    # return ppaca_votes
    json_data = open('ppaca.json')
    data = json.load(json_data)
    data2 = json.dumps(data)
    return data2

@app.route('/PPACA')
def render3():
    return render_template('ppaca.html')

# @app.route('/PPACA/senate/json')
# def rendeter_ppaca_senate_json():
#     d = vote_funding_analysis.senate_funding('s396-111.2009', 2006, 2008, 2010, 'H%')

#     yea = d['Yea']
#     nay = d['Nay']

#     ppaca_votes = [{'name': 'Yea', 'children': yea, 'color': '#1F8A70'},\
#     {'name': 'Nay', 'children': nay, 'color': '#BEDB39'}]
#     ppaca_votes = json.dumps(ppaca_votes)

#     return ppaca_votes

# @app.route('/PPACA/senate')
# def render_ppaca_senate():
#     return render_template('ppaca_senate.html')



if __name__ == "__main__":
    app.run(debug=True)
