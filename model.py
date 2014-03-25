from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from operator import itemgetter
import os


# create engine

# engine = create_engine("sqlite:///moneypolitics.db", echo=False)
print os.environ.get("DATABASE_URL")
engine = create_engine(os.environ.get("DATABASE_URL"))
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

#class declarations

# data from OpenSecrets
class Candidate(Base):
    # creating a candidate object to be added to the database
    __tablename__ = "candidates"

    id = Column(Integer, primary_key = True)
    cycle = Column(String(4))
    fec_cand_id = Column(String(9))
    cid = Column(String(9))
    first_last_p = Column(String(50))
    party = Column(String(1))
    # dist_id_run_for = Column(String(4))
    # dist_id_curr = Column(String(4))
    # curr_cand = Column(String(1))
    # cycle_cand = Column(String(1))
    crpico = Column(String(1))
    recip_code = Column(String(2))
    # nopacs = Column(String(1))

class Committee(Base):
	# creating a committee object to be added to the database
	__tablename__ = "committees"

	id = Column(Integer, primary_key = True)
	cycle = Column(String(4))
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
	# foreign = Column(Integer) # how do I do a 'bit' field? i think it's something I have to import
	active = Column(Integer(1))

class Individual(Base):
	# creating an individual object to be added to the database
	__tablename__ = "individuals"
    
	id = Column(Integer, primary_key = True)
	cycle = Column(String(4))
	fec_trans_id = Column(String(19)) # 7 chars before 2012
	contrib_id = Column(String(12))
	contrib = Column(String(50)) # this field was 34 chars before 2012
	recip_id = Column(String(9))
	org_name = Column(String(50)) # 40
	ult_org = Column(String(50)) # 40
	real_code = Column(String(5))
	# date = Column(DateTime) 
	amount = Column(Integer) 
	# street = Column(String(40))
	# city = Column(String(30)) # 18
	# state = Column(String(2))
	zip_code = Column(String(5))
	recip_code = Column(String(2))
	type = Column(String(3))
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
	cycle = Column(String(4))
	fec_rec_no = Column(String(19)) # 7 chars before 2012
	pac_id = Column(String(9))
	# cid = Column(String(9), ForeignKey('candidates.cid'))
	cid = Column(String(9))
	amount = Column(Integer) # previoulsy an integer
	# date = Column(String) # DATES!
	real_code = Column(String(5))
	type = Column(String(3))
	di = Column(String(1))
	fec_cand_id = Column(String(9))

	# candidate = relationship('candidate', backref=backref('candidates', order_by=id))

class PAC_other(Base):
	__tablename__ = "pacother"
	# creating a PAC-other object to be added to the database

	id = Column(Integer, primary_key = True)
	cycle = Column(String(4))
	fec_rec_no = Column(String(19)) # 7 chars before 2012
	filer_id = Column(String(9))
	donor_cmte = Column(String(50)) # 40
	contrib_lend_trans = Column(String(50)) # 40
	# city = Column(String(30)) # 40
	# state = Column(String(2))
	# zip_code = Column(String(5))
	fec_occ_emp = Column(String(38)) # 35
	prim_code = Column(String(5))
	# date = Column(DateTime)
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
	# from legislators-current.csv or legislators-historic.csv
	__tablename__ = "legislator"

	# creating a member object to be added to the database

	# I probably need to give these all lengths?
	
	id = Column(Integer, primary_key = True)
	last_name = Column(String)
	first_name = Column(String)
	birthday = Column(DateTime(), nullable = True)
	gender = Column(String(1))
	position_type = Column(String(3))
	state = Column(String(2))
	party = Column(String)
	# url = Column(String)
	# address = Column(String)
	# phone = Column(String)
	# contact_form = Column(String)
	# rss_url = Column(String)
	# twitter = Column(String)
	# facebook = Column(String)
	# facebook_id = Column(String)
	# youtube = Column(String)
	# youtube_id = Column(String)
	bioguide_id = Column(String)
	thomas_id = Column(String)
	opensecrets_id = Column(String)
	lis_id = Column(String)
	# cspan_id = Column(String)
	govtrack_id = Column(String)
	# votesmart_id = Column(String)
	# ballotpedia_id = Column(String)
	# washington_post_id = Column(String)
	# icpsr_id = Column(String)
	# wikipedia_id = Column(String)
	# senate_votes = relationship('SenateVote')

class Bill(Base):
	# creating an object in the Bill table
	__tablename__ = "bill"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	bill_title = Column(String)
	bill_popular_title = Column(String)
	bill_short_title = Column(String)
	bill_subject = Column(String)
	bill_sponsor = Column(String)

class Sponsor(Base):
	# creating an object sponsor table - creates a relationship between Legislators and Bills
	__tablename__ = "legislator_bill_sponsor"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	thomas_id = Column(String)


class Subjects(Base):
	# creating a record in the Subjects table to track the subjects of various bills, will have many entries for the same bill
	__tablename__ = "bill_subjects"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	bill_subject = Column(String)


class HouseVote(Base):
	__tablename__ = "legislator_bill_house_vote"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	thomas_id = Column(String)
	bill_id = Column(String)
	vote_value = Column(String) #Column(ENUM('Aye', 'No', 'Yea', 'Nay', 'Present', 'Not Voting'))

class SenateVote(Base):
	__tablename__ = "legislator_bill_senate_vote"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	lis_id = Column(String) #(String, ForeignKey('legislator.lis_id'))
	bill_id = Column(String)
	vote_value = Column(String) #Column(ENUM('Aye', 'No', 'Yea', 'Nay', 'Present', 'Not Voting'))

	# legislator = relationship("Legislator", backref=backref('legislator', order_by=id))

class Vote(Base):
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
	chamber = Column(String)
	startdate = Column(DateTime)
	enddate = Column(DateTime)
	party = Column(String)
	state = Column(String(2))
	district = Column(Integer)


def main():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()