from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy.sql import text
from sqlalchemy import func
from operator import itemgetter
import os


# create engine

# engine = create_engine("sqlite:///moneypolitics.db", echo=False)

engine = create_engine(os.environ.get("DATABASE_URL"))
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


## class declarations


class Candidate(Base):
	"""Create a candidate object to take in data from the FEC 
	Candidates file (data/CampainFin/CampaignFinYY/candsYY.txt) 
	and add it to the database on the candidates table.
	"""
	__tablename__ = "candidates"

	id = Column(Integer, primary_key = True)
	cycle = Column(Integer(4))
	fec_cand_id = Column(String(9))
	cid = Column(String(9))
	first_last_p = Column(String(50))
	party = Column(String(1))
	dist_id_run_for = Column(String(4))
	dist_id_curr = Column(String(4))
	curr_cand = Column(String(1))
	cycle_cand = Column(String(1))
	crpico = Column(String(1))
	recip_code = Column(String(2))
	nopacs = Column(String(1))

class Committee(Base):
	"""Create a committee object to take in data from the FEC 
	Committees file (data/CampaignFin/CampaignFinYY/cmtesYY.txt)
	and add it to the database on the committees table.
	"""
	__tablename__ = "committees"

	id = Column(Integer, primary_key = True)
	cycle = Column(Integer(4))
	cmte_id = Column(String(9))
	pac_short = Column(String(50))
	affiliate = Column(String(50), nullable = True)
	recip_id =  Column(String(9))
	recip_code = Column(String(2))
	fec_cand_id = Column(String(9))
	party = Column(String(1))
	prim_code = Column(String(5))
	source = Column(String)
	active = Column(Integer(1))

class Individual(Base):
	"""Create an individual object to take in data from the FEC
	Committees file (data/CampaignFin/CampaignFinYY/indivsYY.txt)
	and add it to the database on the individuals table.
	"""
	__tablename__ = "individuals"
    
	id = Column(Integer, primary_key = True)
	cycle = Column(Integer(4))
	fec_trans_id = Column(String(19)) # 7 chars before 2012
	contrib_id = Column(String(12))
	contrib = Column(String(50)) # this field was 34 chars before 2012
	recip_id = Column(String(9))
	recip_link_to = Column(String)
	org_name = Column(String(50)) # 40
	real_code = Column(String(5))
	amount = Column(Integer) 
	zip_code = Column(String(5))
	recip_code = Column(String(2))
	transaction_type = Column(String(3))
	cmte_id = Column(String(9))
	other_id = Column(String(9))
	occupation = Column(String(38)) # called Occ_EF
	employer = Column(String(38))# called Emp_EF
	source = Column(String(5))

class PAC(Base):
	"""Create a PAC object to take in data from the FEC Committees
	file (data/CampaignFin/CampaignFinYY/pacsYY.txt) and add it to
	the database on the pacs table.
	"""
	__tablename__ = "pacs"

	id = Column(Integer, primary_key = True)
	cycle = Column(Integer(4))
	fec_rec_no = Column(String(19)) # 7 chars before 2012
	pac_id = Column(String(9))
	cid = Column(String(9))
	amount = Column(Integer) # previoulsy an integer
	date = Column(DateTime, nullable = True) # DATES!
	real_code = Column(String(5))
	transaction_type = Column(String(3))
	di = Column(String(1))
	fec_cand_id = Column(String(9))

class PAC_other(Base):
	"""Create a PAC-Other object to take in data from the FEC 
	Committees file (data/CampaignFin/CampaignFinYY/pac_otherYY.txt)
	and add it to the database on the pacother table.
	"""
	__tablename__ = "pacother"

	id = Column(Integer, primary_key = True)
	cycle = Column(Integer(4))
	fec_rec_no = Column(String(19)) # 7 chars before 2012
	filer_id = Column(String(9))
	donor_cmte = Column(String(50)) # 40
	# contrib_lend_trans = Column(String(50)) # 40
	# city = Column(String(30)) # 40
	# state = Column(String(2))
	# zip_code = Column(String(5))
	fec_occ_emp = Column(String(38)) # 35
	prim_code = Column(String(5))
	date = Column(DateTime, nullable = True)
	amount = Column(Integer) # previously Number(Double)
	recip_id = Column(String(9))
	party = Column(String(1))
	other_id = Column(String(9))
	recip_code = Column(String(2))
	recip_prim_code = Column(String(5))
	# amend = Column(String(1))
	# report = Column(String(3))
	# pg = Column(String(1))
	# microfilm = Column(String(11))
	transaction_type = Column(String(3))
	real_code = Column(String(5))
	# source = Column(String(5))


class Legislator(Base):
	"""Create a legislator object to take in data from the legslator
	.yaml files
	(data/peole_data/legislators-current.yaml and legislators-historical.yaml) 
	and add it to the database on the legislators table.  

	Will be used primarily connect data points with different ID types 
	(i.e. connecting CampaignFin data that uses the govtrack_id with 
	voting data that uses either the bioguide_id or the lis_id).
	"""
	__tablename__ = "legislators"

	
	id = Column(Integer, primary_key = True)
	last_name = Column(String)
	first_name = Column(String)
	official_full = Column(String)
	birthday = Column(DateTime(), nullable = True)
	gender = Column(String(1))
	bioguide_id = Column(String)
	thomas_id = Column(Integer)
	opensecrets_id = Column(String)
	lis_id = Column(String)
	govtrack_id = Column(Integer)
	

class Bill(Base):
	"""Create a bill object to take in data from the bill .json files
	(data/congress/[congress]/bills/[bill type]/[bill id]/data.json) 
	and add it to the database on the bills table. 
	"""
	__tablename__ = "bills"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	bill_title = Column(String)
	bill_popular_title = Column(String)
	bill_short_title = Column(String)
	bill_subject = Column(String)
	bill_sponsor = Column(String)

class Sponsor(Base):
	"""Create a sponsor object to take in data from the bill .json files
	(data/congress/[congress]/bills/[bill type]/[bill id]/data.json) and
	add it to the database on the sponsors table. 

	Will be used primarily to connect legislators to bills they have
	sponsored.
	"""
	__tablename__ = "bill_sponsors"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	thomas_id = Column(Integer)


class Subjects(Base):
	"""Create a subject object to take in data from the bill .json files
	(data/congress/[congress]/bills/[bill type]/[bill id]/data.json) and
	add it to the database on the subjects table. 

	Will be used to connect bills to relevent funding sources.
	"""
	__tablename__ = "bill_subjects"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	bill_subject = Column(String)


class LegislatorBillVote(Base):
	"""Create a LegislatorBillVote object to take in data from the vote 
	.json files (data/congress/[congress]/vote/[year]/[vote_id]/data.json) 
	and add it to the database on the legislator_bill_votes table. 

	Used to connect legislators to bills.

	Ultimately deprecated to split voting info into house votes and senate
	votes because they reference different ids on the legislator table.
	"""
	__tablename__ = "legislator_bill_votes"


	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	reference_id = Column(String) # indicates whether to join 
	# legislators on bioguide_id or lis_id
	legislator_id = Column(String)  # either bioguide_id or lis_id
	bill_id = Column(String)
	vote_value = Column(String)

class HouseVote(Base):
	"""Create a HouseVote object to take in data from the vote .json 
	files (data/congress/[congress]/vote/[year]/[vote_id]/data.json) 
	and add it to the database on the legislator_bill__house_votes 
	table. 

	Used to connect the value of a legislator's vote (Yea, Nay, Aye, 
	No, Present, Not Voting, etc) to a particular bill.
	"""
	__tablename__ = "legislator_bill_house_votes"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	bioguide_id = Column(String)
	bill_id = Column(String)
	vote_value = Column(String)

class SenateVote(Base):
	"""Create a SenateVote object to take in data from the vote .json 
	files (data/congress/[congress]/vote/[year]/[vote_id]/data.json) 
	and add it to the database on the legislator_bill__senate_votes 
	table. 

	Used to connect value of a legislator's vote (Yea, Nay, Aye, No, 
	Present, Not Voting, etc) to a particular bill.
	"""
	__tablename__ = "legislator_bill_senate_votes"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	lis_id = Column(String)
	bill_id = Column(String)
	vote_value = Column(String) 

class Vote(Base):
	"""Create a Vote object to take in data from the vote .json files 
	(data/congress/[congress]/vote/[year]/[vote_id]/data.json) 
	and add it to the database on the votes table. 

	Will be used for information (category, result) for particular votes.
	"""
	__tablename__ = "votes"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	bill_id = Column(String)
	date = Column(DateTime)
	vote_category = Column(String)
	vote_result = Column(String)


class LegislatorLegacy(Base):
	"""Create a LegislatorLegacy object to take in data from the vote 
	.json files (data/congress/[congress]/vote/[year]/[vote_id]/data.json) 
	and add it to the database on the votes table. 

	Used for information (category, result) for particular votes.
	"""
	__tablename__ = "legislator_legacy"

	id = Column(Integer, primary_key = True)
	govtrack_id = Column(Integer)
	term_type = Column(String)
	start = Column(DateTime)
	end = Column(DateTime)
	party = Column(String)
	state = Column(String(2))
	district = Column(Integer)
	senate_class = Column(String)
	state_rank = Column(String)

class CRP_ID(Base):
	"""Create a CRP_ID object to take in data from the CRP_IDs.csv file
	(data/CampaignFin/CRP_IDs.csv) and add it to the crp_ids table.

	Used for translating real_codes and prim_codes on Campaign Finance
	tables (candidates, committees, individuals, pacs, pacothers) into 
	sectors.
	"""
	__tablename__ = "crp_ids"

	id = Column(Integer, primary_key = True)
	catcode = Column(String(5))
	catname = Column(String)
	catorder = Column(String(3))
	industry = Column(String)
	sector = Column(String)
	sector_long = Column(String)

class Legislators113(Base):
	"""Create a Legslators113 object to take in data from 
	legislators-current (data/people_data/legislators-current.csv)
	and add it to the legislators113 table.

	Used to generate current list of legislators.
	"""
	__tablename__ = "legislators113"

	id = Column(Integer, primary_key = True)
	govtrack_id = Column(Integer)
	opensecrets_id = Column(String)
	thomas_id = Column(Integer)
	bioguide_id = Column(String)
	last_name = Column(String)
	first_name = Column(String)
	term_type = Column(String)
	state = Column(String)
	party = Column(String)

class Legislators113Districts(Base):
	"""Create Legislators113Districts object to take in data from the
	CRP_IDs_districts file (data/people_data/CRP_IDs_districts.csv) and
	add it to the legislators113districts table.

	Used in conjunction with the legislators113 table to generate the
	current_legislators table.
	"""

	__tablename__='legislators113districts'
	id = Column(Integer, primary_key = True)
	opensecrets_id = Column(String)
	district = Column(String)


## functions

def get_all_current():
	"""Generates a list of all current legislators including chamber,
	party, and disctrict (senators are given districts in the format
	state 2-character abbreviation followed by S1 or S2 depending on
	whether they are the junior or senior senator).  Uses the
	current_legislators view.
	"""
	query = """SELECT * 
			   FROM current_legislators 
			   ORDER BY term_type, \
			   district"""

	return session.execute(query)


def get_sectors(opensecrets_id):
	"""Generates a current legislator's funding by sector for the 2012
	and 2014 campaign cycles using the donations_113 view in the
	database.  Only references donations made by individuals.
	"""

	sectors = session.execute(
				text("""SELECT sum(d.amount) as size, c.sector as name
						FROM donations_113 as d, crp_ids as c
						WHERE d.real_code = c.catcode
						AND d.recip_id = :opensecrets_id
						GROUP BY c.sector
						ORDER BY size DESC"""),
					{'opensecrets_id':opensecrets_id})
	return sectors

def make_json(opensecrets_id):
	"""
	"""
	sectors = session.execute(
				text("""SELECT sum(d.amount) as size, c.sector as name
						FROM donations_113 as d, crp_ids as c
						WHERE d.real_code = c.catcode
						AND d.recip_id = :opensecrets_id
						GROUP BY c.sector
						ORDER BY size DESC"""),
					{'opensecrets_id':opensecrets_id})
	sector_list = []
	sector_total = 0
	for sector in sectors:
		# come up with hex values for each category
		sector_total += float(sector['size'])
		color_value = int(sector['size'])/10
		sector_list.append({'name': sector['name'], 'size': sector['size']})
	offset = (200^2)/(float(sector_list[0]['size'])/float(sector_total))
	for sector in sector_list:
		# print [float(sector['size']), float(sector_total), \
		# 	(float(sector['size'])/float(sector_total))]
		sector['color'] = 'rgb(' +  str(int(float(sector['size'])/\
			float(sector_total)))+ ',89,' + str(int((float(sector['size'])/\
			float(sector_total))*offset)) + ')'
	return sector_list


def get_subject_votes(legislator):
	pass


def get_all_amounts(opensecrets_id):
	"""For a particular member of congress specified by their opensecrets_id, 
	return a dictionary with sectors as keys and total donation amount as 
	corresponding values by calling the relevent query for PACs, PACother, 
	and Individuals and then merge them together in a single dictionary.
	"""
	# function to take data from queries to create contribution dictionary
	def sum_all_amounts(contributor_list, key, amount_dict, key_dict):
		for c in contributor_list:
			name = key_dict[c[key]]
			if not amount_dict.get(name):
				amount_dict[name] = 0
			amount_dict[name] += c['sum_amount']

	pacs = session.execute(
		text('''SELECT sum(amount) AS sum_amount, real_code
				FROM pacs p
				WHERE cid = :opensecrets_id
				AND (cycle = 2012 or cycle=2014)
				GROUP BY real_code'''),
			{'opensecrets_id': opensecrets_id})
	pacothers = session.execute(
		text('''SELECT sum(amount) AS sum_amount, prim_code
				FROM pacother
				WHERE recip_id = :opensecrets_id
				AND (cycle = 2012 or cycle=2014)
				GROUP BY prim_code'''),
			{'opensecrets_id': opensecrets_id})
	individuals = session.execute(
		text('''SELECT sum(amount) AS sum_amount, real_code
				FROM individuals
				WHERE recip_id = :opensecrets_id
				AND (cycle = 2012 or cycle=2014)
				GROUP BY real_code'''),
			{'opensecrets_id': opensecrets_id})
	sectors = session.execute(
			text('''SELECT catcode AS code, sector AS name
					FROM crp_ids''')
	)

	sector_dict = dict([(s['code'], s['name']) for s in sectors])

	pacs = list(pacs)
	print ['pacs',pacs]
	pacothers = list(pacothers)
	print ['pacothers', pacothers]
	individuals = list(individuals)
	print ['individuals',individuals]

	amount_dict = {}

	sum_all_amounts(individuals, 'real_code', amount_dict, sector_dict)
	sum_all_amounts(pacs, 'real_code', amount_dict, sector_dict)
	sum_all_amounts(pacothers, 'prim_code', amount_dict, sector_dict)

	return amount_dict

def make_json2(opensecrets_id):
	"""Takes the data returned by the get_all_amounts for a particular member
	of congressfunction and creates a json object to be used to generate a 
	bubble chart with the bubble.html template.
	"""
	# returns the list of keys in the dict of sectors and amounts
	# generated by get_all_amounts
	sector_dict = get_all_amounts(opensecrets_id)
	# get the keys from that dictionary
	sector_keys = sector_dict.keys()
	# instantiates the total as )
	sector_total = 0
	# instantiates the list that will be populated by the for loops below
	sector_list = []
	# adds the sector as a value assciated with the key 'name'
	# and the amount as a value associated with the key 'size'
	for sector in sector_keys:
		sector_total += float(sector_dict[sector])
		# color_value = int(sector_dict[sector])/10
		sector_list.append({'name': sector, 'size': sector_dict[sector]})
	# come up with hex values for each category
	offset = (10)/(float(sector_list[0]['size'])/float(sector_total))
	for sector in sector_list:
		# print [float(sector['size']), float(sector_total), \
		# 	(float(sector['size'])/float(sector_total))]
		sector['color'] = 'rgb(' +  str(int(float(sector['size'])/\
			float(sector_total)))+ ',89,' + str(int((float(sector['size'])/\
			float(sector_total))*offset)) + ')'
	return sector_list




def main():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()