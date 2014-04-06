moneypolitics
=============
Creating a database with information about Campaign Funding information and bills and votes in Congress to look at relationship between where members of congress get their funding and how they vote on relevent legislation.

Overview
----------------------
Having used databases without understanding them, I wanted to explore the process of creating and filling a database with data that was not my own.  I am also interested in the ways in which technology can be used for the greater social good (see [here](http://usatoday30.usatoday.com/tech/news/story/2012-07-20/pothole-app/56367586/1) for inspiration).  By bringing all of the relevent information together, I learned not only about what goes into building a database but also about how to make the information in the database is accessible and meaningful.

I sourced my Campaign Finance data from [OpenSecrets.org](http://www.opensecrets.org/) and the information on bills and votes from [GovTrack.us](https://www.govtrack.us/).  Knowing that the scope of what I wanted to accomplish might be out of the range of four weeks of work but that this is a topic I find interesting enough to continue working for some time, I included financing data going back to 1994 and bill/vote data going back to 1999 to give myself the room to explore what might ultimatley be gleaned from having a larger base of information.  I wrote scripts to parse my data (written in python to parse csv, json, xml and yaml) and discovered along the way that data from the government, while certainly available, cannot be relied up to be clean or normalized.  And the process of cleaning and normalizing data can become extensive.
