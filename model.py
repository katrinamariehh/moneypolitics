from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy.sql import text
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


#class declarations

# data from OpenSecrets
class Candidate(Base):
    # creating a candidate object to be added to the database
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
	# creating a committee object to be added to the database
	__tablename__ = "committees"

	id = Column(Integer, primary_key = True)
	cycle = Column(Integer(4))
	cmte_id = Column(String(9))
	pac_short = Column(String(50))
	affiliate = Column(String(50), nullable = True)
	# ult_org = Column(String(50))
	recip_id =  Column(String(9))
	recip_code = Column(String(2))
	fec_cand_id = Column(String(9))
	party = Column(String(1))
	prim_code = Column(String(5))
	source = Column(String)
	# sensitive = Column(String(1))
	# foreign = Column(Integer)
	active = Column(Integer(1))

class Individual(Base):
	# creating an individual object to be added to the database
	__tablename__ = "individuals"
    
	id = Column(Integer, primary_key = True)
	cycle = Column(Integer(4))
	fec_trans_id = Column(String(19)) # 7 chars before 2012
	contrib_id = Column(String(12))
	contrib = Column(String(50)) # this field was 34 chars before 2012
	recip_id = Column(String(9))
	recip_link_to = Column(String)
	org_name = Column(String(50)) # 40
	# ult_org = Column(String(50)) # 40
	real_code = Column(String(5))
	# date = Column(DateTime) 
	amount = Column(Integer) 
	# street = Column(String(40))
	# city = Column(String(30)) # 18
	# state = Column(String(2))
	zip_code = Column(String(5))
	recip_code = Column(String(2))
	transaction_type = Column(String(3))
	cmte_id = Column(String(9))
	other_id = Column(String(9))
	# gender = Column(String(1))
	# fec_occ_emp = Column(String(35)) 	# before 2012 only
	# microfilm  = Column(String(11))
	occupation = Column(String(38)) # called Occ_EF
	employer = Column(String(38))# called Emp_EF
	source = Column(String(5))

class PAC(Base):
	__tablename__ = "pacs"
	# creating a PAC object to be added to the database
	
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
	__tablename__ = "pacother"
	# creating a PAC-other object to be added to the database

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
	# from legislators-current.yaml and legislators-historical.yaml
	__tablename__ = "legislators"

	# creating a member object to be added to the database

	# I probably need to give these all lengths?
	
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
	# creating an object in the Bill table
	__tablename__ = "bills"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	bill_title = Column(String)
	bill_popular_title = Column(String)
	bill_short_title = Column(String)
	bill_subject = Column(String)
	bill_sponsor = Column(String)

class Sponsor(Base):
	# creating an object sponsor table - creates a relationship 
	# between Legislators and Bills
	__tablename__ = "bill_sponsors"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	thomas_id = Column(Integer)


class Subjects(Base):
	# creating a record in the Subjects table to track the subjects 
	# of various bills, will have many entries for the same bill
	__tablename__ = "bill_subjects"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	bill_subject = Column(String)


class LegislatorBillVote(Base):
	# creating a table to hold each house member's vote by bill
	__tablename__ = "legislator_bill_votes"
	# __tablename__ = "legislator_bill_house_votes"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	reference_id = Column(String) # indicates whether to join 
	# legislators on bioguide_id or lis_id
	legislator_id = Column(String)  # either bioguide_id or lis_id
	bill_id = Column(String)
	vote_value = Column(String)

class HouseVote(Base):
	__tablename__ = "legislator_bill_house_votes"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	bioguide_id = Column(String)
	bill_id = Column(String)
	vote_value = Column(String)

class SenateVote(Base):
	# creating a table to hold each senator's vote by bill
	__tablename__ = "legislator_bill_senate_votes"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	lis_id = Column(String)
	bill_id = Column(String)
	vote_value = Column(String) 

class Vote(Base):
	# creating a table 
	__tablename__ = "votes"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	bill_id = Column(String)
	date = Column(DateTime)
	vote_category = Column(String)
	vote_result = Column(String)


class LegislatorLegacy(Base):
	# creating an object for each member's past service periods
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
    __tablename__ = "crp_ids"

    id = Column(Integer, primary_key = True)
    catcode = Column(String(5))
    catname = Column(String)
    catorder = Column(String(3))
    industry = Column(String)
    sector = Column(String)
    sector_long = Column(String)

class Legislators113(Base):
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
	__tablename__='legislators113districts'
	id = Column(Integer, primary_key = True)
	opensecrets_id = Column(String)
	district = Column(String)


## functions
def get_all_current():
	query = """SELECT * 
			   FROM current_legislators 
			   ORDER BY term_type, \
			   district"""

	return session.execute(query)


def get_sectors(opensecrets_id):
	sectors = session.execute(
				text("""SELECT sum(d.amount) as total, c.sector
						FROM donations_113 as d, crp_ids as c
						WHERE d.real_code = c.catcode
						AND d.recip_id = :opensecrets_id
						GROUP BY c.sector
						ORDER BY c.sector"""),
					{'opensecrets_id':opensecrets_id})
	# sector_dict = {}
	# for sector in sectors:
	# 	key = sector['sector']
	# 	value = sector['total']
	# 	sector_dict[key] = value
	# print sector_dict
	return sectors

def make_json(opensecrets_id):
	sectors = session.execute(
				text("""SELECT sum(d.amount) as size, c.sector as name
						FROM donations_113 as d, crp_ids as c
						WHERE d.real_code = c.catcode
						AND d.recip_id = :opensecrets_id
						GROUP BY c.sector
						ORDER BY size"""),
					{'opensecrets_id':opensecrets_id})
	sector_list = []
	for sector in sectors:
		# come up with hex values for each category
		color_value = int(sector['size'])/10
		sector_list.append({'name': sector['name'], 'size': sector['size'],\
		 'color:': (color_value, color_value, color_value)})
	print sector_list
	return sector_list


def get_subject_votes(legislator):
	pass



def main():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()