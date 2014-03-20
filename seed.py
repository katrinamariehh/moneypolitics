
# with CSV reader, pipes may be quote characters--try this tomorrow reading in one CampaignFin14 file

# you can map a zip to a dictionary--use this for passing in headers

# xmltodict to parse the xml data in the people_legacy file to a dictionary to send into the database--I should be able to easily read dictionaries into the database, right?

# I think i need to just throw all of the votes and bills into a the database and start dealing with it

import model
import csv
import datetime
import json
import os
import path_feed



# def load_CampaignFin_cands(session):
#     with open('data/CampaignFin/CampaignFin14/cands14.txt') as f:
#         reader = csv.reader(f, delimiter = ",", quotechar = "|")
#         for row in reader:
#         # setting row info from file as an object to go into the database
#             cand_Cycle, cand_FECCandID, cand_CID, cand_FirstLastP, cand_Party, cand_DistIDRunFor, cand_DistIDCurr, cand_CurrCand, cand_CycleCand, cand_CRPICO, cand_RecipCode, cand_NoPacs = row
#             cand = model.Candidate(Cycle=cand_Cycle,
#             					   FECCandID=cand_FECCandID,
#             					   CID=cand_CID,
#             					   FirstLastP=cand_FirstLastP,
#             					   Party=cand_Party,
#             					   # DistIdRunFor=cand_DistIdRunFor,
#             					   # CurrCand=cand_CurrCand,
#             					   # CycleCand=cand_CycleCand,
#             					   CRPICO=cand_CRPICO,
#             					   RecipCode=cand_RecipCode)
#             session.add(cand)
#     session.commit()

# def load_CampaignFin_cmtes(session):
# 	with open('data/CampaignFin/CampaignFin14/cmtes14.txt') as f:
# 		reader = csv.reader(f, delimiter = ',', quotechar = '|')
# 		for row in reader:
# 		# setting row info from file as an object to add to the database
# 			cmte_Cycle, cmte_CmteID, cmte_PACShort, cmte_Affiliate, cmte_Ultorg, cmte_RecipID, cmte_RecipCode, cmte_FECCandID, cmte_Party, cmte_PrimCode, cmte_Source, cmte_Sensitive, cmte_Foreign, cmte_Active = row
# 			# if I want to use Ultorg I have to fix the unicode thing (run seed and inlude Ultorg and you'll see the error)
# 			# cmte_Ultorg = unicode(cmte_Ultorg)
# 			try:
# 				cmte = model.Committee(Cycle=cmte_Cycle,
# 									   CmteID=cmte_CmteID,
# 									   PACShort=cmte_PACShort,
# 									   Affiliate=cmte_Affiliate,
# 									   # Ultorg=cmte_Ultorg,
# 									   RecipID=cmte_RecipID,
# 									   RecipCode=cmte_RecipCode,
# 									   FECCandID=cmte_FECCandID,
# 									   Party=cmte_Party,
# 									   PrimCode=cmte_PrimCode,
# 									   Source=cmte_Source,
# 									   # Sensitive=cmte_Sensitive,
# 									   # Foreign=cmte_Foreign,
# 									   Active=cmte_Active)
# 				session.add(cmte)
# 				session.commit()
# 			except:
# 				print row
# 				break
	

def loadCampaignFin_indiv(session):
	with open('test.txt') as f:
		reader = csv.reader(f, delimiter = ',', quotechar = '|')
		for row in reader:
		# setting row info from file as an object to add to the database
			indiv_Cycle, indiv_FECTransID, indiv_ContribID, indiv_Contrib, indiv_RecipID, indiv_Orgname, indiv_UltOrg, indiv_RealCode, indiv_Date, indiv_Amount, indiv_Street, indiv_City, indiv_State, indiv_ZIP, indiv_RecipCode, indiv_Type, indiv_CmteID, indiv_OtherID, indiv_Gender, indiv_Microfilm, indiv_Occupation, indiv_Employer, indiv_Source = row

			# indiv_Cycle, indiv_FECTransID, indiv_ContribID, indiv_Contrib, indiv_RecipID, indiv_Orgname, indiv_UltOrg, indiv_RealCode, indiv_Date, indiv_Amount, indiv_Street, indiv_City, indiv_State, indiv_ZIP, indiv_RecipCode, indiv_Type, indiv_CmteID, indiv_OtherID, indiv_Gender, indiv_FecOccEmp, indiv_Microfilm, indiv_Occupation, indiv_Employer, indiv_Source fields before 2012

			indiv = model.Individual(Cycle=indiv_Cycle, 
									 FECTransID=indiv_FECTransID, 
									 ContribID=indiv_ContribID, 
									 Contrib=indiv_Contrib, 
									 RecipID=indiv_RecipID, 
									 Orgname=indiv_Orgname, 
									 UltOrg=indiv_UltOrg, 
									 RealCode=indiv_RealCode, 
									 Date=indiv_Date, 
									 Amount=indiv_Amount, 
									 Street=indiv_Street, 
									 City=indiv_City, 
									 State=indiv_State, 
									 ZIP=indiv_ZIP, 
									 RecipCode=indiv_RecipCode, 
									 Type=indiv_Type, 
									 CmteID=indiv_CmteID, 
									 OtherID=indiv_OtherID, 
									 Gender=indiv_Gender,
									 Microfilm=indiv_Microfilm, 
									 Occupation=indiv_Occupation, 
									 Employer=indiv_Employer, 
									 Source=indiv_Source)
			session.add(indiv)
	session.commit()

# def loadCampaignFin_PAC(session):
# 	with open('data/CampaignFin/CampaignFin[YY]/pacs[YY].txt') as f:
# 		reader = csv.reader(f, delimiter = ',', quotechar = '|')
# 		for row in reader:
# 		# setting row info from file as an object to add to the database
# 			PAC_Cycle, PAC_FECRecNo, PAC_PACID, PAC_CID, PAC_Amount, PAC_Date,PAC_RealCode, PAC_Type, PAC_DI, PAC_FECCandID = row
# 			PAC = model.PAC(Cycle=PAC_Cycle, 
# 							FECRecNO=PAC_FECRecNo, 
# 							PACID=PAC_PACID, 
# 							CID=PAC_CID, 
# 							Amount=PAC_Amount, 
# 							Date=PAC_Date, 
# 							RealCode=PAC_RealCode, 
# 							Type=PAC_Type, 
# 							DI=PAC_DI, 
# 							FECCandID=PAC_FECCandID)
# 			session.add(PAC)
# 	session.commit()

# def loadCampaignFin_PAC_other(session):
# 	with open('data/CampaginFin/CampaignFin[YY]/pac_other[YY].txt')
# 		reader = csv.reader(f, delimiter = ',', quotechar = '|')
# 		for row in reader:
# 		# setting row info from file as an object to add to the database
# 			PAC_other_Cycle, PAC_other_FECRecNo, PAC_other_Filerid, PAC_other_ContribLendTrans, PAC_other_City, PAC_other_State, PAC_other_ZIP, PAC_other_FECOccEmp, PAC_other_Primcode, PAC_other_Date, PAC_other_Amount, PAC_other_RecipID, PAC_other_Party, PAC_other_Otherid, PAC_other_RecipCode, PAC_other_RecipPrimcode, PAC_other_Amend, PAC_other_Report, PAC_other_PG, PAC_other_Microfilm, PAC_other_Type, PAC_other_RealCode, PAC_other_Source = row
# 			PAC_other = model.PAC_other(Cycle=PAC_other_Cycle, 
# 										FECRecNo=PAC_other_FECRecNo, 
# 										Filerid=PAC_other_Filerid, 
# 										# ContribLendTrans=PAC_other_ContribLendTrans,
# 										City=PAC_other_City, 
# 										State=PAC_other_State, 
# 										ZIP=PAC_other_ZIP, 
# 										FECOccEmp=PAC_other_FECOccEmp,
# 										PrimCode=PAC_other_Primcode, 
# 										Date=PAC_other_Date, 
# 										Amount=PAC_other_Amount, 
# 										RecipID=PAC_other_RecipID, 
# 										Party=PAC_other_Party, 
# 										Otherid=PAC_other_Otherid, 
# 										RecipCode=PAC_other_RecipCode,
# 										PrimCode=PAC_other_RecipPrimcode,
# 										# Amend=PAC_other_Amend, 
# 										# Report=PAC_other_Report, 
# 										# PG=PAC_other_PG, 
# 										# Microfilm=PAC_other_Microfilm, 
# 										# Type=PAC_other_Type, 
# 										RealCode=PAC_other_RealCode,
# 										# Source=PAC_other_Source)
# 			session.add(PAC_other)
# 	session.commit()
# # to load a json file and dump it to a dictionary, use json.load()

# def load_bills(session):
# 	# function to create bill objects to database
# 	b = open([congress]/[bills]/[hr or s]/[hr or s][number])
# 	bill_dict = json.load(b)

# 	# sponsor data needs to go into a different table (sponsors)--can I create records in different tables in the same function?
# 	sponsor = bill_dict['sponsor]']['thomas_id']
# 	cosponsors_list = bill_dict['cosponsors']
# 	cosponsors_ids = [sponsor]
# 	for cosponsor in cosponsor_list:
# 		cosponsors.append(cosponsor['thomas_id'])
# 	cosponsors = cosponsor_ids
# 	for cosponsor in cosponsors:
# 		if cosponsor.index(cosponsor) = 0:
# 			is_primary = True
# 		else:
# 			is_primary = False
# 		Sponsor = model.Sponsor(bill_id=bill_id,
# 								thomas_id=cosponsor
# 								is_primary=is_primary)
# 		session.add(Sponsor)



# 	# this info needs to go on the bill table
# 	bill_id = bill_dict['bill_id']
# 	bill_title = bill_dict['titles'][0]['title']
# 	# bill_type = bill_dict['bill_type']
# 	# bill_congress = bill_dict['congress']
# 	# bill_number = bill_dict['number']
# 	bill_popular_title = bill_dict['popular_title']
# 	bill_short_title = bill_dict['short_title']
	
# 	# this info needs to go into a subjects table with the bill id
# 	top_subject = bill_dict['subjects_top_term']
# 	subjects = bill_dict['subjects']
	
# 	Bill = model.Bill(bill_id=bill_id,
# 					  bill_title=bill_title,
# 					  bill_popular_title=bill_popular_title,
# 					  bill_short_title=bill_short_title,
# 					  bill_subject=top_subject
# 					  )
# 	session.add(Bill)

# 	for subject in subjects:
# 		Subjects = model.Subject(bill_id=bill_id,
# 								 subject=subject)
# 		session.add(Subject)
# 	session.commit()


# def load_votes(session):
# 	# votes are essentially a way to connect legislators to bills
# 	v = open([congress]/[votes]/[year]/[h or s]/[h or s][number])
# 	vote_dict = json.load(v)

# 	# creating the bill_id
# 	vote_bill = vote_dict['bill']['type']
# 	vote_bill_number = vote_dict['number']
# 	vote_bill_congress = vote_dict['congress']
# 	vote_bill_id = vote_bill + vote_bill_number + vote_bill_congress
# 	# will need to reference bill id and vote category
# 	# I probably only care about one category of vote

# 	vote_id = vote_dict['vote_id']
# 	vote_category = vote_dict['category']
# 	vote_result = vote_dict['result']
# 	Vote = model.Vote(vote_id=vote_id,
# 					  vote_category=vote_category,
# 					  vote_result=vote_result)
# 	session.add(Vote)

# 	vote_types = vote_dict['votes'].keys() # a dictionary where the keys are 'Yea', 'Nay', 'Present', 'Not Voting' (but not all votes are the same in this respect--some have 'Aye' and 'No')
# 	for vote_type in vote_types:
# 		legislator_ids = [] # how can I use the iterator name in the variable name? I don't think this is correct.
# 		voters = vote_dict['votes'][vote_type]
# 		for voter in voters:
# 			legislator_ids.append(voter['id'])
# 		for legislator in legislator_ids:
# 			LegislatorBillVote = model.LegislatorBillVote(vote_id=vote_id,
# 							  				thomas_id=legislator,
# 											bill_id=vote_bill_id,
# 											vote_value=vote_type)
# 			session.add(LegislatorBillVote)

# 	session.commit()

def main(session):
	# load_CampaignFin_cands(session)
	# load_CampaignFin_cmtes(session)
	loadCampaignFin_indiv(session)

if __name__ == "__main__":
    main(model.session)