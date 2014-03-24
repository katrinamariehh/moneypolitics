from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from operator import itemgetter


# create engine

engine = create_engine("sqlite:///moneypolitics.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

#class declarations

# data from OpenSecrets
class Candidate(Base):
    # creating a candidate object to be added to the database
    __tablename__ = "Candidates"

    id = Column(Integer, primary_key = True)
    Cycle = Column(String(4))
    FECCandID = Column(String(9))
    CID = Column(String(9))
    FirstLastP = Column(String(50))
    Party = Column(String(1))
    # DistIdRunFor = Column(String(4))
    # DistIDCurr = Column(String(4))
    # CurrCand = Column(String(1))
    # CycleCand = Column(String(1))
    CRPICO = Column(String(1))
    RecipCode = Column(String(2))
    # NoPacs = Column(String(1))

class Committee(Base):
	# creating a committee object to be added to the database
	__tablename__ = "Committees"

	id = Column(Integer, primary_key = True)
	Cycle = Column(String(4))
	CmteID = Column(String(9))
	PACShort = Column(String(50))
	Affiliate = Column(String(50), nullable = True)
	# Ultorg = Column(String(50))
	RecipID =  Column(String(9))
	RecipCode = Column(String(2))
	FECCandID = Column(String(9))
	Party = Column(String(1))
	PrimCode = Column(String(5))
	Source = Column(String(5))
	# Sensitive = Column(String(1))
	# Foreign = Column(Integer) # how do I do a 'bit' field? i think it's something I have to import
	Active = Column(Integer(1))

class Individual(Base):
	# creating an individual object to be added to the database
	__tablename__ = "Individuals"
    
	id = Column(Integer, primary_key = True)
	Cycle = Column(String(4))
	FECTransID = Column(String(19)) # 7 chars before 2012
	ContribID = Column(String(12))
	Contrib = Column(String(50)) # this field was 34 chars before 2012
	RecipID = Column(String(9))
	Orgname = Column(String(50)) # 40
	UltOrg = Column(String(50)) # 40
	RealCode = Column(String(5))
	Date = Column(DATETIME) # date objects OH GOD DO I HAVE TO DO DATETIME STUFF AGAIN?
	Amount = Column(Integer) # not sure how this will work? integer w/out length?
	Street = Column(String(40))
	City = Column(String(30)) # 18
	State = Column(String(2))
	ZIP = Column(String(5))
	RecipCode = Column(String(2))
	Type = Column(String(3))
	CmteID = Column(String(9))
	OtherID = Column(String(9))
	Gender = Column(String(1))
	FecOccEmp = Column(String(35)) 	# before 2012 only
	Microfilm  = Column(String(11))
	Occupation = Column(String(38)) # called Occ_EF
	Employer = Column(String(38))# called Emp_EF
	Source = Column(String(5))

class PAC(Base):
	__tablename__ = "PACs"
	# creating a PAC object to be added to the database
	
	id = Column(Integer, primary_key = True)
	Cycle = Column(String(4))
	FECRecNo = Column(String(19)) # 7 chars before 2012
	PACID = Column(String(9))
	CID = Column(String(9))
	Amount = Column(Integer) # previoulsy an integer
	Date = Column(String) # DATES!
	RealCode = Column(String(5))
	Type = Column(String(3))
	DI = Column(String(1))
	FECCandID = Column(String(9))

class PAC_other(Base):
	__tablename__ = "PAC Other"
	# creating a PAC-other object to be added to the database

	id = Column(Integer, primary_key = True)
	Cycle = Column(String(4))
	FECRecNo = Column(String(19)) # 7 chars before 2012
	Filerid = Column(String(9))
	DonorCmte = Column(String(50)) # 40
	ContribLendTrans = Column(String(50)) # 40
	City = Column(String(30)) # 40
	State = Column(String(2))
	ZIP = Column(String(5))
	FECOccEmp = Column(String(38)) # 35
	PrimCode = Column(String(5))
	Date = Column(DATETIME)
	Amount = Column(Integer) # previously Number(Double)
	RecipID = Column(String(9))
	Party = Column(String(1))
	Otherid = Column(String(9))
	RecipCode = Column(String(2))
	RecipPrimCode = Column(String(5))
	# Amend = Column(String(1))
	# Report = Column(String(3))
	# PG = Column(String(1))
	# Microfilm = Column(String(11))
	# Type = Column(String(3))
	RealCode = Column(String(5))
	# Source = Column(String(5))

class Legislator(Base):
	# from legislators-current.csv or legislators-historic.csv
	__tablename__ = "Legislator"

	# creating a member object to be added to the database

	# I probably need to give these all lengths?
	
	id = Column(Integer, primary_key = True)
	last_name = Column(String)
	first_name = Column(String)
	birthday = Column(String)
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

class LegislatorLegacy(Base):
	# creating an object for each member's past service periods
	__tablename__ = "LegislatorLegacy"

	id = Column(Integer, primary_key = True)
	govtrack_id = Column(Integer)
	chamber = Column(String)
	startdate = Column(DATETIME)
	enddate = Column(DATETIME)
	party = Column(String)
	state = Column(String(2))
	district = Column(Integer)

class Bill(Base):
	# creating an object in the Bill table
	__tablename__ = "Bill"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	bill_title = Column(String)
	bill_popular_title = Column(String)
	bill_short_title = Column(String)
	bill_subject = Column(String)
	bill_sponsor = Column(String)

class Sponsor(Base):
	# creating an object sponsor table - creates a relationship between Legislators and Bills
	__tablename__ = "LegislatorBillSponsor"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	thomas_id = Column(String)



class Subjects(Base):
	# creating a record in the Subjects table to track the subjects of various bills, will have many entries for the same bill
	__tablename__ = "BillSubjects"

	id = Column(Integer, primary_key = True)
	bill_id = Column(String)
	bill_subject = Column(String)


class HouseVote(Base):
	__tablename__ = "LegislatorBillHouseVote"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	thomas_id = Column(String)
	bill_id = Column(String)
	vote_value = Column(String) #Column(ENUM('Aye', 'No', 'Yea', 'Nay', 'Present', 'Not Voting'))

class SenateVote(Base):
	__tablename__ = "LegislatorBillSenateVote"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	thomas_id = Column(String)
	bill_id = Column(String)
	vote_value = Column(String) #Column(ENUM('Aye', 'No', 'Yea', 'Nay', 'Present', 'Not Voting'))

class Vote(Base):
	__tablename__ = "Votes"

	id = Column(Integer, primary_key = True)
	vote_id = Column(String)
	bill_id = Column(String)
	date = Column(DATETIME)
	vote_category = Column(String)
	vote_result = Column(String)


def main():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()