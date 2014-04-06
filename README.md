moneypolitics
=============
Creating a database with information about Campaign Funding and records of bills and votes in Congress to look at relationship between where members of congress get their funding and how they vote on relevent legislation.

Overview
----------------------
Having used databases without understanding them, I wanted to explore the process of creating and filling a database with data that was not my own.  I am also interested in the ways in which technology can be used for the greater social good (see [here](http://usatoday30.usatoday.com/tech/news/story/2012-07-20/pothole-app/56367586/1) for inspiration).  By bringing all of the relevent information together, I learned not only about what goes into building a database but also about how to make the information in the database is accessible and meaningful.

I sourced my Campaign Finance data from [OpenSecrets.org](http://www.opensecrets.org/) and the information on bills and votes from [GovTrack.us](https://www.govtrack.us/).  Knowing that the scope of what I wanted to accomplish might be out of the range of four weeks of work but that this is something I want to keep working on, I included financing data going back to 1994 and bill/vote data going back to 1999 to give myself the room to explore what might ultimatley be gleaned from having a larger base of information.  

I wrote scripts to parse my data (written in python to parse csv, json, xml and yaml) and used SQLAlchemy to fill my PostgreSQL database.  To make the data meaningful and accesible, I built an app on top of it to allow some exploration of the information available as well as some pre-determined points of interest to display.

Technology Used
----------------------
- scripts for building and seeding the database are written in Python using SQLAlchemy with PostgreSQL serving as the database engine
- visualizations use the [d3js.org](d3js.org) library (JavaScript)
- the webapp uses the Flask framework and is made to look prettier with Bootstrap

Limitations
----------------------
Becaue the dataset is quite large, this repository contains all of the files needed to recreate the project exclusive of the actual data needed to seed the database.  The [rsync_commands.py](https://github.com/katrinamariehh/moneypolitics/blob/master/rsync_commands.py) file contains a script for generating rsync requests for bill and vote data from GovTrack.us, all Campaign Finance records can be downloaded from on OpenSecrets.org, and additional files from GovTrack (legislators-current.yaml, legislators-historical.yaml, legislators-current.csv) can be found [here](https://www.govtrack.us/data/congress-legislators/).  The CRP IDs file (used for interpreting the Campaign Finance coding) can be downloaded from OpenSecrets [here](http://www.opensecrets.org/resources/create/api_doc.php).

Useability
----------------------
In it's current state, users can access 2012 and 2014 donation information for all current legislators as well as a table or visualized as a bubble chart.  Additionally, visualizations for selected bills (The Patient Protection and Affordable Care Act (2010) and the Troubled Asset Relief Program (2008)) show votes for and against each bill with the size of each legislator's bubble representative of contributions received from relevent sectors (Health in the case of PPACA, Finance in the case of TARP).
[screenshots]

Future Plans
----------------------
- expanding the vote-funding visualization to include all bills available
- pulling data across all legislators to determine if/how campagin funding can be used to predict voting patterns regardless of other political motivations (i.e. a decision tree that shows that X amount of dollars will lead with some certainty to a particular voting pattern when the bill is in regards to a particular topic)
- determining what other meaning can be pulled from the aggregated data using statistical anaylsis--k-means, pearson correlations, etc.
