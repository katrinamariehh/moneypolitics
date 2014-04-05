
import model
import csv
import datetime
import json
import os
from path_feed import fpaths, cpaths
from bs4 import BeautifulSoup
import yaml



def create_finance_list(path):
	"""Create a list of file paths for the Campaign Finance files to
	be read and loaded into the database.
	"""

	path_list = []
	contents = os.listdir(path)

	for node in contents:
		# ignore files that start with .
		if node[0] == '.':
			continue
		fullpath = path+'/'+node
		# if it's a directory, keep reading
		if os.path.isdir(fullpath):
			path_list += create_finance_list(fullpath)
		else:
		# if it's a file, add the path to the list
			path_list.append(fullpath)
	return path_list

# an empty dictionary to add the Campaign Finance paths to based on type
fpaths = {}

def parse_finance_list(list):
	"""A function to separate the Campaign Finance filepaths by type 
	in order to be read by different seed functions.
	"""

	# define the different empty lists to append the path strings to
	fpaths['cands'] = []
	fpaths['cmtes'] = []
	fpaths['indivs'] = []
	fpaths['pac_other'] = []
	fpaths['pacs'] = []

	for path in list:
		# add candidate file paths to the candidate list
		if 'cands' in path:
			fpaths['cands'].append(path)
		# add committee file paths to the committee list
		if 'cmtes' in path:
			fpaths['cmtes'].append(path)
		# add individual file paths to the individual list
		if 'indivs' in path:
			fpaths['indivs'].append(path)
		# add the pac file paths to the pac list
		if 'pac_' in path:
			fpaths['pac_other'].append(path)
		# ad the pacs_other file paths to the pacs_other list
		if 'pacs' in path:
			fpaths['pacs'].append(path)
	return fpaths



def create_congress_list(path):
	"""Create a list of file paths for the congress files to be read
	and loaded into the database.
	"""

	# create a path list for the congressional records
	path_list = []
	contents = os.listdir(path)
	# skip the follwoing nodes--they are less important bills, links to text 
	# files, etc.
	nodes_to_skip = ['hconres', 'hjres', 'hres', 'sconres', 'sjres', 'sres']
	for node in contents:
		if node[0] == '.' or node in nodes_to_skip or node[-4:] == '.xml' or node[0:4] == 'text':
			continue
		fullpath = path+'/'+node
		if os.path.isdir(fullpath):
			path_list += create_congress_list(fullpath)
		else:
			path_list.append(fullpath)
	return path_list

# create an empty dictionary to add votes and bills as different separate 
# lists which will be fed to different functions in the seed
cpaths = {}


def parse_congress_list(list):
	"""A function to separate the congress filepaths by type 
	in order to be read by different seed functions.
	"""
	# instantiate the empty values in the dictionary
	cpaths['votes'] = []
	cpaths['bills'] = []

	for path in list:
		# add the path to either votes or bills based on which one appears  
		# in the path string
		if 'votes' in path:
			cpaths['votes'].append(path)
		if 'bills' in path:
			cpaths['bills'].append(path)

	return cpaths


def load_CampaignFin_cands(session):
	"""Parsing the candidates csv files to add as Candidate objects
	on the candidates table in the database using the path files
	created by create_finance_list and parse_finance_list.
	"""

    # paths = ['data/CampaignFin/CampaignFin08/cands08.txt']#TEST
    # for path in paths: #TEST

    for path in fpaths['cands']:
    

    	# open each file in the list with the CSV reader
	    with open(path) as f:
	        reader = csv.reader(f, delimiter = ",", quotechar = "|")
			# starting a counter to commit regularly throughout the process
	        counter = 0

	        for row in reader:
	        	counter += 1
	        # setting row info from file as an object to go into the database
	        	Cycle, FECCandID, CID, FirstLastP, Party, DistIDRunFor, \
	        	DistIDCurr, CurrCand, CycleCand, CRPICO, RecipCode, NoPacs = row

	        	cand = model.Candidate(cycle=Cycle,
	            					   fec_cand_id=FECCandID,
	            					   cid=CID,
	            					   first_last_p=FirstLastP,
	            					   party=Party,
	            					   dist_id_run_for=DistIDRunFor,
	            					   dist_id_curr=DistIDCurr,
	            					   curr_cand=CurrCand,
	            					   cycle_cand=CycleCand,
	            					   crpico=CRPICO,
	            					   recip_code=RecipCode,
	            					   nopacs=NoPacs)
	        	session.add(cand)
	        	if counter % 500 == 0:
	        		session.commit
	        		# print "I've committed %s candidates" % counter
	        		# break
    session.commit()

def load_CampaignFin_cmtes(session):
	"""Parsing the committees csv files to add as Committee objects
	on the committees table in the database using the path files
	created by create_finance_list and parse_finance_list.
	"""
	# paths = ['data/CampaignFin/CampaignFin08/cmtes08.txt'] #TEST
	# for path in paths: #TEST

	for path in fpaths['cmtes']:

		# open each file in the list
		with open(path) as f:
			reader = csv.reader(f, delimiter = ',', quotechar = '|')
			# starting a counter to commit regularly throughout the process
			counter = 0
			for row in reader:
				counter += 1
			# setting row info from file as an object to add to the database
				Cycle, CmteID, PACShort, Affiliate, UltOrg, RecipID, \
				RecipCode, FECCandID, Party, PrimCode, Source, Sensitive, \
				Foreign, Active = row

				cmte = model.Committee(cycle=Cycle,
										   cmte_id=CmteID,
										   pac_short=PACShort,
										   affiliate=Affiliate,
										   recip_id=RecipID,
										   recip_code=RecipCode,
										   fec_cand_id=FECCandID,
										   party=Party,
										   prim_code=PrimCode,
										   source=Source,
										   active=Active)
				session.add(cmte)
				if counter % 500 == 0:
					session.commit()

			session.commit()

	

def loadCampaignFin_indiv(session):
	"""Parsing the individuals csv files to add as Individual objects
	on the individuals table in the database using the path files
	created by create_finance_list and parse_finance_list.
	"""
	# paths = ['data/CampaignFin/CampaignFin08/indivs08-1.txt'] #TEST
	# for path in paths: #TEST

	for path in fpaths['indivs']:		

		# open each file in the list
		with open(path) as f:
			reader = csv.reader(f, delimiter = ',', quotechar = '|')
			# starting a counter to commit regularly throughout the process
			counter = 0

			# if statement to separately parse files before or after 2012
			if path[-6:-4] == '12' or path[-6:-4] == '14':

				for row in reader:
					counter += 1


				# setting row info from file as an object to add to the database

					Cycle, FECTransID, ContribID, Contrib, RecipID, Orgname, \
					UltOrg, RealCode, Date, Amount, Street, City, State, ZIP, \
					RecipCode, Type, CmteID, OtherID, Gender, Microfilm, \
					Occupation, Employer, Source = row

					# removing data that will cause unicode errors
					try:
						Orgname = Orgname.decode('utf-8')
						UltOrg = UltOrg.decode('utf-8')
						Contrib = Contrib.decode('utf-8')
						Employer = Employer.decode('utf-8')
						Occupation = Occupation.decode('utf-8')

					except UnicodeDecodeError:
						Orgname = None
						UltOrg = None
						Contrib = None
						Employer = None
						Occupation = None

					# if statement to declare which table to link to
					# either committee or candidate depending on the
					# starting character of the recip_id
					if RecipID != '' and RecipID[0] == 'C':
						link_to = "committee"
					else:
						link_to = "candidate"

					indiv = model.Individual(cycle=Cycle, 
											 fec_trans_id=FECTransID, 
											 contrib_id=ContribID, 
											 contrib=Contrib, 
											 recip_id=RecipID, 
											 org_name=Orgname, 
											 real_code=RealCode, 
											 amount=Amount, 
											 zip_code=ZIP, 
											 recip_code=RecipCode, 
											 recip_link_to=link_to,
											 transaction_type=Type, 
											 cmte_id=CmteID, 
											 other_id=OtherID, 
											 occupation=Occupation, 
											 employer=Employer, 
											 source=Source)
					session.add(indiv)
					
					if counter % 500 == 0:
						session.commit()

						
			# parsing files before 2012
			else:
				for row in reader:
					counter += 1

					# dealing with a data error
					if counter == 2612896:
						continue

					else:
						Cycle, FECTransID, ContribID, Contrib, RecipID,\
						Orgname, UltOrg, RealCode, Date, Amount, Street, \
						City, State, ZIP, RecipCode, Type, CmteID, OtherID, \
						Gender, FecOccEmp, Microfilm, Occupation, Employer, \
						Source = row

					# removing data that will cause unicode errors
						try:
							Orgname = Orgname.encode('utf-8')
							UltOrg = UltOrg.encode('utf-8')
							Contrib = Contrib.encode('utf-8')
							Employer = Employer.encode('utf-8')
							Occupation = Occupation.decode('utf-8')

						except UnicodeDecodeError:
							Orgname = None
							UltOrg = None
							Contrib = None
							Employer = None
							Occupation = None

						# if statement to declare which table to link to
						# either committee or candidate depending on the
						# starting character of the recip_id
						if RecipID != '' and RecipID[0] == 'C':
							link_to = "committee"
						else:
							link_to = "candidate"

						indiv = model.Individual(cycle=Cycle, 
												 fec_trans_id=FECTransID, 
												 contrib_id=ContribID, 
												 contrib=Contrib, 
												 recip_id=RecipID, 
												 org_name=Orgname, 
												 real_code=RealCode, 
												 amount=Amount, 
												 zip_code=ZIP, 
												 recip_code=RecipCode, 
												 recip_link_to=link_to,
												 transaction_type=Type, 
												 cmte_id=CmteID, 
												 other_id=OtherID,  
												 occupation=Occupation, 
												 employer=Employer, 
												 source=Source)
						session.add(indiv)
						if counter % 500 == 0:
							session.commit()


		session.commit()


def loadCampaignFin_PAC(session):
	"""Parsing the pacs csv files to add as PAC objects
	on the pacs table in the database using the path files
	created by create_finance_list and parse_finance_list.
	"""
	# paths = ['data/CampaignFin/CampaignFin08/pacs08.txt'] #TEST
	# for path in paths:
	for path in fpaths['pacs']:
	
		# open each file in the list
		with open(path) as f:
			reader = csv.reader(f, delimiter = ',', quotechar = '|')
			# starting a counter to commit regularly throughout the process
			counter = 0
			for row in reader:
				counter +=1
			# setting row info from file as an object to add to the database
				Cycle, FECRecNo, PACID, CID, Amount, Date, RealCode, Type, \
				DI, FECCandID = row
				
				if Date != "":
					Date = datetime.datetime.strptime(Date, "%m/%d/%Y")
				else:
					Date = None

				PAC = model.PAC(cycle=Cycle, 
								fec_rec_no=FECRecNo, 
								pac_id=PACID, 
								cid=CID, 
								amount=Amount, 
								date=Date, 
								real_code=RealCode, 
								transaction_type=Type, 
								di=DI, 
								fec_cand_id=FECCandID)
				session.add(PAC)
				if counter % 500 == 0:
					session.commit()
					# print "I've committed %s individuals" % counter
					# break
	session.commit()

def loadCampaignFin_PAC_other(session):
	"""Parsing the pac_other csv files to add as PAC_other objects
	on the pacother table in the database using the path files
	created by create_finance_list and parse_finance_list.
	"""
	# paths = ['data/CampaignFin/CampaignFin08/pac_other08.txt'] #TEST
	# for path in paths: #TEST
	for path in fpaths['pac_other']:
		# using the paths generated by path_feed, open each path
		with open(path) as f:
			# read in each file in the list
			reader = csv.reader(f, delimiter = ',', quotechar = '|')
			# starting a counter to commit regularly throughout the process
			counter = 0
			for row in reader:

			# setting row info from file as an object to add to the database
				Cycle, FECRecNo, Filerid, DonorCmte, ContribLendTrans, City, \
				State, ZIP, FECOccEmp, Primcode, Date, Amount, RecipID, Party, \
				Otherid, RecipCode, RecipPrimcode, Amend, Report, PG, Microfilm, \
				Type, RealCode, Source = row
				
				if Date != "":
					Date = datetime.datetime.strptime(Date, "%m/%d/%Y")
				else:
					Date = None

				Amount = float(Amount)

				PAC_other = model.PAC_other(cycle=Cycle, 
											fec_rec_no=FECRecNo, 
											filer_id=Filerid,
											donor_cmte=DonorCmte,
											fec_occ_emp=FECOccEmp,
											prim_code=Primcode, 
											date=Date, 
											amount=Amount, 
											recip_id=RecipID, 
											party=Party, 
											other_id=Otherid, 
											recip_code=RecipCode,
											recip_prim_code=RecipPrimcode,
											transaction_type=Type, 
											real_code=RealCode)
				session.add(PAC_other)
				if counter % 500 == 0:
					session.commit()
	session.commit()



def load_bills(session):
	"""Parsing the bills json files to add Bill, Sponsor, and Subject
	objects onto their respective tables in the database using the path files
	created by create_congress_list and parse_congress_list.
	"""
	# function to create bill objects to database	
	# test_list = ['data/congress/109/bills/hr/hr5194/data.json', 
	# 			   'data/congress/109/bills/hr/hr731/data.json', 
	# 			   'data/congress/108/bills/hr/hr1951/data.json', 
	# 			   'data/congress/113/bills/s/s120/data.json', 
	# 			   'data/congress/107/bills/hr/hr354/data.json', 
	# 			   'data/congress/108/bills/hr/hr458/data.json', 
	# 			   'data/congress/109/bills/hr/hr5498/data.json', 
	# 			   'data/congress/110/bills/s/s2407/data.json', 
	# 			   'data/congress/108/bills/s/s672/data.json', 
	# 			   'data/congress/110/bills/s/s3424/data.json', 
	# 			   'data/congress/109/bills/hr/hr2883/data.json', 
	# 			   'data/congress/107/bills/hr/hr5016/data.json', 
	# 			   'data/congress/112/bills/hr/hr2693/data.json', 
	# 			   'data/congress/112/bills/s/s2319/data.json', 
	# 			   'data/congress/113/bills/hr/hr1530/data.json', 
	# 			   'data/congress/108/bills/hr/hr1651/data.json', 
	# 			   'data/congress/109/bills/hr/hr3898/data.json', 
	# 			   'data/congress/109/bills/hr/hr1803/data.json', 
	# 			   'data/congress/113/bills/hr/hr334/data.json', 
	# 			   'data/congress/112/bills/hr/hr731/data.json', 
	# 			   'data/congress/113/bills/s/s487/data.json', 
	# 			   'data/congress/112/bills/hr/hr3189/data.json', 
	# 			   'data/congress/113/bills/s/s1174/data.json', 
	# 			   'data/congress/112/bills/hr/hr854/data.json', 
	# 			   'data/congress/107/bills/hr/hr2977/data.json', 
	# 			   'data/congress/106/bills/hr/hr396/data.json', 
	# 			   'data/congress/107/bills/hr/hr2192/data.json', 
	# 			   'data/congress/109/bills/s/s2212/data.json', 
	# 			   'data/congress/113/bills/hr/hr2336/data.json', 
	# 			   'data/congress/109/bills/hr/hr5068/data.json'] #TEST
	# starting a counter to commit regularly throughout the process
	counter = 0
	# for bill in test_list: #TEST

	for bill in cpaths['bills']:

		counter += 1
		b = open(bill)
		# loading the contents of the file as a dictionary to acess specific parts
		bill_dict = json.load(b)

		# declaring variables from the file contents to us as parts of the objects below
		bill_id = bill_dict['bill_id']
		bill_title = bill_dict['titles'][0]['title']
		bill_popular_title = bill_dict['popular_title']
		bill_short_title = bill_dict['short_title']
		
		# adding a Bill object

		Bill = model.Bill(bill_id=bill_id,
						  bill_title=bill_title,
						  bill_popular_title=bill_popular_title,
						  bill_short_title=bill_short_title,
						  bill_subject=top_subject
						  )
		session.add(Bill)

		# data for the Sponsor object
		sponsor = bill_dict['sponsor']['thomas_id']
		cosponsor_list = bill_dict['cosponsors']
		cosponsor_ids = [sponsor]


		# generating the list of cosponsors to add as Sponsor objects
		for cosponsor in cosponsor_list:
			cosponsor_ids.append(cosponsor['thomas_id'])

		# adding the individual cosponsors as Sponsor objects
		for cosponsor in cosponsor_ids:
			Sponsor = model.Sponsor(bill_id=bill_id,
									thomas_id=cosponsor)
			session.add(Sponsor)

		# generating the list of subjects to be added as Subject objects
		subjects = bill_dict['subjects']

		# adding the subjects as Subject objects
		for subject in subjects:
			Subject = model.Subjects(bill_id=bill_id,
									bill_subject=subject)
			session.add(Subject)
		
		if counter % 500 == 0:
			session.commit()
	session.commit()


def load_votes(session):
	"""Parsing the votes json files to add Vote, HouseVote, and 
	SenateVote objects onto their respective tables in the database 
	using the path files created by create_congress_list and 
	parse_congress_list.
	"""
	# test_list = ['data/congress/108/votes/2004/h177/data.json', 
	# 			 'data/congress/112/votes/2011/s153/data.json', 
	# 			 'data/congress/112/votes/2011/h183/data.json', 
	# 			 'data/congress/110/votes/2007/h1118/data.json', 
	# 			 'data/congress/110/votes/2007/h774/data.json', 
	# 			 'data/congress/110/votes/2008/h34/data.json', 
	# 			 'data/congress/107/votes/2001/h335/data.json', 
	# 			 'data/congress/109/votes/2006/h328/data.json', 
	# 			 'data/congress/111/votes/2010/h392/data.json', 
	# 			 'data/congress/111/votes/2009/s209/data.json', 
	# 			 'data/congress/106/votes/1999/h319/data.json', 
	# 			 'data/congress/108/votes/2003/h173/data.json', 
	# 			 'data/congress/110/votes/2008/s52/data.json', 
	# 			 'data/congress/112/votes/2011/h344/data.json', 
	# 			 'data/congress/113/votes/2013/h66/data.json', 
	# 			 'data/congress/113/votes/2013/s178/data.json', 
	# 			 'data/congress/112/votes/2011/h783/data.json', 
	# 			 'data/congress/107/votes/2002/h87/data.json', 
	# 			 'data/congress/110/votes/2007/h778/data.json', 
	# 			 'data/congress/110/votes/2007/h336/data.json', 
	# 			 'data/congress/108/votes/2003/h497/data.json', 
	# 			 'data/congress/109/votes/2005/h513/data.json', 
	# 			 'data/congress/110/votes/2007/s113/data.json', 
	# 			 'data/congress/113/votes/2013/h53/data.json', 
	# 			 'data/congress/111/votes/2010/h326/data.json', 
	# 			 'data/congress/111/votes/2009/h498/data.json', 
	# 			 'data/congress/109/votes/2005/s36/data.json', 
	# 			 'data/congress/111/votes/2010/s191/data.json', 
	# 			 'data/congress/110/votes/2007/h735/data.json', 
	# 			 'data/congress/107/votes/2002/h20/data.json'] #TEST

	# starting a counter to commit regularly throughout the process
	counter = 0
	# for vote in test_list: #TEST

	for vote in cpaths['votes']:
		counter += 2
		# open the file
		v = open(vote)
		# load as a json object to access values
		vote_dict = json.load(v)

		# skip votes related to types of bills not being stored
		votes_to_skip = ['hconres', 'hjres', 'hres', 'sconres', 'sjres', 'sres']
		
		# iterate over votes to add associated information to the database
		if vote_dict.get('bill') and vote_dict['bill']['type'] not in votes_to_skip:
			# creating the bill_id
			vote_bill = str(vote_dict['bill']['type'])
			vote_bill_number = str(vote_dict['bill']['number'])
			vote_bill_congress = str(vote_dict['congress'])
			vote_bill_id = vote_bill + vote_bill_number + '-' + vote_bill_congress
			
			# changing the date into a datetime object
			vote_date = datetime.datetime.strptime(vote_dict['date'][0:10], "%Y-%m-%d")

			# assign variables to be added as part of the Vote object
			vote_id = vote_dict['vote_id']
			vote_category = vote_dict['category']
			vote_result = vote_dict['result']

			creat Vote object
			Vote = model.Vote(vote_id=vote_id,
							  bill_id=vote_bill_id,
							  date=vote_date,
							  vote_category=vote_category,
							  vote_result=vote_result)
			session.add(Vote)

			# creating HouseVote and SenateVote objects (connecting 
			# Legislators with the value of their vote--House votes 
			# reference the GovTrack id, Senate votes reference the LIS ID)

			# a dictionary where the keys are the type of vote (Yea/Nay/etc)
			vote_types = vote_dict['votes'].keys() 
			
			# add each member's vote as a HouseVote or SenateVote object
			for vote_type in vote_types:
				legislator_ids = []
				voters = vote_dict['votes'][vote_type]

				# add each legislator's id to the list to be added as 
				# part of the object
				for voter in voters:
					try:
						legislator_ids.append(voter['id'])
					except:
						print vote_bill_id
				
				# add object attributes as HouseVote or SenateVote objects
				for legislator in legislator_ids:
					# commented code below was used when all votes were on a single table
					# if vote_id[0] == 'h':
					# 	reference_id='bioguide_id'
					# elif vote_id[0] == 's':
					# 	reference_id='lis_id'

					# LegislatorBillVote = model.LegislatorBillVote(vote_id=vote_id,
					# 											  bill_id=vote_bill_id,
					# 											  vote_value=vote_type,
					# 											  reference_id=reference_id,
					# 											  legislator_id=legislator)
							
					if vote_id[0] == 'h':
						LegislatorBillVote = model.HouseVote(vote_id=vote_id,
										  				bioguide_id=legislator,
														bill_id=vote_bill_id,
														vote_value=vote_type)
						session.add(LegislatorBillVote)
					if vote_id[0] == 's':
						LegislatorBillVote = model.SenateVote(vote_id=vote_id,
										  				lis_id=legislator,
														bill_id=vote_bill_id,
														vote_value=vote_type)
					session.add(LegislatorBillVote)
			if counter % 500:
				session.commit()
		session.commit()


def load_legislators(session):
	"""Parsing the legislator yaml files to add Legislator and 
	LegislatorLegacy objects onto their respective tables in 
	the database.
	"""
	file_paths = ['data/people_data/legislators-historical.yaml', 
				  'data/people_data/legislators-current.yaml']

	for path in file_paths:
		l = open(path)
		l_list = yaml.load(l)
		
		# starting a counter to commit regularly throughout the process
		counter = 0

		for legislator in l_list:
			counter += 1
			# getting data needed to add legislator object
			last_name = legislator['name'].get('last')
			first_name = legislator['name'].get('first')
			official_full = legislator['name'].get('official_full')

			# checking if gender/birthday information are available
			if legislator.get('bio'):
				gender = legislator['bio'].get('gender')
				# converting birthdate into a datetime object
				if legislator['bio'].get('birthday'):
					birthday = datetime.datetime.strptime(legislator['bio'].get('birthday'), "%Y-%m-%d")
				else:
					birthday = None
			else:
				gender = None
				birthday = None
			
			bioguide_id = legislator['id'].get('bioguide')
			thomas_id = legislator['id'].get('thomas')
			opensecrets_id = legislator['id'].get('opensecrets')
			lis_id = legislator['id'].get('lis')
			govtrack_id = legislator['id'].get('govtrack')
			if thomas_id: 
				Legislator = model.Legislator(last_name=last_name,
											  first_name=first_name,
											  official_full=official_full,
											  birthday=birthday,
											  gender=gender,
											  bioguide_id=bioguide_id,
											  thomas_id=thomas_id,
											  opensecrets_id=opensecrets_id,
											  lis_id=lis_id,
											  govtrack_id=govtrack_id)
				session.add(Legislator)
			# getting a legislator's terms to add as LegislatorLegacy objects
			terms = legislator['terms']
			for term in terms:
				term_type = term.get('type')
				start = datetime.datetime.strptime(term.get('start'), "%Y-%m-%d")
				end = datetime.datetime.strptime(term.get('end'), "%Y-%m-%d")
				state = term.get('state')
				district = term.get('district')
				party = term.get('party')
				senate_class = term.get('class')
				state_rank = term.get('state_rank')

				if start > datetime.datetime(1955, 12, 13):

					LegislatorLegacy = model.LegislatorLegacy(govtrack_id=govtrack_id,
															  term_type=term_type,
															  start=start,
															  end=end,
															  state=state,
															  district=district,
															  party=party,
															  senate_class=senate_class,
															  state_rank=state_rank)
					session.add(LegislatorLegacy)

			if counter % 50 == 0:
				session.commit()


def load_crp_ids(session):
	"""Reading in CRP_ID information from a csv file to add as 
	CRP_ID objects.
	"""

    with open('data/CampaignFin/CRP_IDs.csv') as f:
        reader = csv.reader(f, delimiter=',')
        f.readline()

        for row in reader:
            Catcode,Catname,Catorder,Industry,Sector,Sector_Long = row

            CRP_ID = model.CRP_ID(catcode=Catcode,
                                  catname=Catname,
                                  catorder=Catorder,
                                  industry=Industry,
                                  sector=Sector,
                                  sector_long=Sector_Long)
            session.add(CRP_ID)

    session.commit()

def load_current(session):
	"""Loading in a list of current members of Congress to add as 
	Legislators113 objects.
	"""
	with open('data/people_data/legislators-current.csv') as f:
		reader = csv.reader(f, delimiter=',')
		f.readline()

		for row in reader:
			last_name, first_name, birthday, gender, term_type, state, party, \
			url, address, phone, contact_form, rss_url, twitter, facebook, \
			facebook_id, youtube, youtube_id, bioguide_id, thomas_id, \
			opensecrets_id, lis_id, cspan_id, govtrack_id, votesmart_id, \
			ballotpedia_id, washington_post_id, icspr_id, wikipedia_id = row

			Current = model.Legislators113(govtrack_id=govtrack_id,
										   opensecrets_id=opensecrets_id,
										   thomas_id=thomas_id,
										   bioguide_id=bioguide_id,
										   last_name=last_name,
										   first_name=first_name,
										   term_type=term_type,
										   state=state,
										   party=party)
			session.add(Current)

	session.commit()

def load_districts(session):
	"""Loading in district information for current members of congress.
	"""

	with open('data/people_data/CRP_IDs_districts.csv') as f:
		reader = csv.reader(f, delimiter=',', quotechar='"')
		f.readline()

		for row in reader:
			try:
				Blank, CID, Name, Party, Office, FECCandID = row
			except ValueError:
				print row
				break

			District = model.Legislators113Districts(opensecrets_id=CID,
													 district=Office
				)
			session.add(District)
	session.commit()



def main(session):
	# f_list = create_finance_list('data/CampaignFin')
	# fpaths = parse_finance_list(f_list)

	# c_list = create_congress_list('data/congress')
	# cpaths = parse_congress_list(c_list)
	
	# load_CampaignFin_cands(session)
	# load_CampaignFin_cmtes(session)
	# loadCampaignFin_indiv(session)
	# loadCampaignFin_PAC(session)
	# loadCampaignFin_PAC_other(session)
	# load_bills(session)
	# load_votes(session)
	# load_legislators(session)
	# load_crp_ids(session)
	# load_legislator_legacy(session)
	# load_current(session)
	# load_districts(session)


if __name__ == "__main__":
    main(model.session)




    