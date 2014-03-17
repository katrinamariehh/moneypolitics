# import stuff

# create engine

Base = declarative_base() # copied this from Ratings exercise
Base.query = session.query_property()

#class declarations

class Candidates(Base):
    # creating a candidate object to be added to the database
    __tablename__ = "Candidate"

    Cycle = Column(String(4))
    FECCandID = Column(String(9))
    CID = Column(String(9))
    FirstLastP = Column(String(50))
    Party = Column(String(1))
    DistIdRunFor = Column(String(4))
    DistIDCurr = Column(String(4))
    CurrCand = Column(String(1))
    CycleCand = Column(String(1))
    CRPICO = Column(String(1))
    RecipCode = Column(String(2))
    NoPacs = Column(String(1))

class Committee(Base):
	# creating a committee object to be added to the database
	__tablename__ = "Committee"

	Cycle = Column(String(4))
	CmteID = Column(String(9))
	PACShort = Column(String(50))
	Affiliate = Column(String(50))
	Ultorg = Column(String(50))
	RecipID =  Column(String(9))
	RecipCode = Column(String(2))
	FECCandID = Column(String(9))
	Party = Column(String(1))
	PrimCode = Column(String(5))
	Source = Column(String(5))
	Sensitive = Column(String(1))
	Foreign = Column(Bit())# how do I do a 'bit' field? i think it's something I have to import
	Active = Column(Integer(1))

class Individuals(Base):
	__tablename__ = "Individual"

	Cycle = Column(String(4))
	FECTransID = Column(String(19)) # 7 chars before 2012
	ContribID = Column(String(12))
	Contrib = Column(String(50)) # this field was 34 chars before 2012
	# this is going to be problematic; there's a comma in the middle and it's delimited by pipes, so it'll be like ',|Hall-Hutzley, Katrina|,'
	RecipID = Column(String(9))
	Orgname = Column(String(50)) # 40
	UltOrg = Column(String(50)) # 40
	RealCode = Column(String(5))
	Date = Column(Date) # date objects OH GOD DO I HAVE TO DO DATETIME STUFF AGAIN?
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