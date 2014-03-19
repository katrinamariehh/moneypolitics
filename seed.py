# the Contrib field on the Indiv table is going to be problematic; there's a comma in the middle and it's delimited by pipes, so it'll be like ',|Hall-Hutzley, Katrina|,'--this will matter in the seed file when I'm loading my rows into my database
# with CSV reader, pipes may be quote characters--try this tomorrow reading in one CampaignFin14 file

# you can map a zip to a dictionary--use this for passing in headers

# xmltodict to parse the xml data in the people_legacy file to a dictionary to send into the database--I should be able to easily read dictionaries into the database, right?

# requests can make http requests for make 

# I think i need to just throw all of the votes and bills into a the database and start dealing with it

import model
import csv
import datetime
import json

def load_CampaignFin_cands(session):
    with open('data/CampaingFin/CampaginFin14/cands14.txt') as f:
        reader = csv.reader(f, delimiter = ",", quotechar = "|")
        for row in reader:
        # setting row info from file as an object to go into the database
            cand_Cycle, cand_FECCandID, cand_CID, cand_FirstLastP, cand_Party, cand_DistIDRunFor, cand_DistIDCurr, cand_CurrCand, cand_CycleCand, cand_CRPICO, cand_RecipCode, cand_NoPacs = row
            cand = model.Candidate(Cycle=cand_Cycle,
            					   FECCandID=cand_FECCandID,
            					   CID=cand_CID,
            					   FirstLastP=cand_FirstLastP,
            					   Party=cand_Party,
            					   DistIdRunFor=cand_DistIdRunFor,
            					   CurrCand=cand_CurrCand,
            					   CycleCand=cand_CycleCand,
            					   CRPICO=cand_CRPICO,
            					   RecipCode=cand_RecipCode)
            session.add(cand)
    session.commit()

def load_CampaignFin_cmtes(session):
	with open('data/CampaignFin/CampaignFin14/cmtes14.txt') as f:
		reader = csv.reader(f, delimiter = ',', quotechar = '|')
		for row in reader:
		# setting row info from file as an object to add to the database
			cmte_Cycle, cmte_CmteID, cmte_PACShort, cmte_Affiliate, cmte_Ultorg, cmte_RecipID, cmte_RecipCode, cmte_FECCandID, cmte_Party, cmte_PrimCode, cmte_Source, cmte_Sensitive, cmte_Foreign, cmte_Active = row
			cmte = model.Committee(Cycle=cmte_Cycle,
								   CmteID=cmte_CmteID,
								   PACShort=cmte_PACShort,
								   Affiliate=cmte_Affiliate,
								   Ultorg=cmte_Ultorg,
								   RecipID=cmte_RecipID,
								   RecipCode=cmte_RecipCode,
								   FECCandID=cmte_FECCandID,
								   Party=cmte_Party,
								   PrimCode=cmte_PrimCode,
								   Source=cmte_Source,
								   Sensitive=cmte_Sensitive,
								   Foreign=cmte_Foreign,
								   Active=cmte_Active)
			session.add(cmte)
	session.commit()

def loadCampaignFin_indiv(session):
	with open('data/CampaignFin/CampaignFin14/indivs14.txt') as f:
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

def loadCampaignFin_PAC(session):
	with open('data/CampaignFin/CampaignFin14/pacs14.txt') as f:
		reader = csv.reader(f, delimiter = ',', quotechar = '|')
		for row in reader:
		# setting row info from file as an object to add to the database
			PAC_Cycle, PAC_FECRecNo, PAC_PACID, PAC_CID, PAC_Amount, PAC_Date,PAC_RealCode, PAC_Type, PAC_DI, PAC_FECCandID = row
			PAC = model.PAC(Cycle=PAC_Cycle, 
							FECRecNO=PAC_FECRecNo, 
							PACID=PAC_PACID, 
							CID=PAC_CID, 
							Amount=PAC_Amount, 
							Date=PAC_Date, 
							RealCode=PAC_RealCode, 
							Type=PAC_Type, 
							DI=PAC_DI, 
							FECCandID=PAC_FECCandID)
			session.add(PAC)
	session.commit()

def loadCampaignFin_PAC_other(session):
	with open('data/CampaginFin/CampaignFin14/pac_other14.txt')
		reader = csv.reader(f, delimiter = ',', quotechar = '|')
		for row in reader:
		# setting row info from file as an object to add to the database
			PAC_other_Cycle, PAC_other_FECRecNo, PAC_other_Filerid, PAC_other_ContribLendTrans, PAC_other_City, PAC_other_State, PAC_other_ZIP, PAC_other_FECOccEmp, PAC_other_Primcode, PAC_other_Date, PAC_other_Amount, PAC_other_RecipID, PAC_other_Party, PAC_other_Otherid, PAC_other_RecipCode, PAC_other_RecipPrimcode, PAC_other_Amend, PAC_other_Report, PAC_other_PG, PAC_other_Microfilm, PAC_other_Type, PAC_other_RealCode, PAC_other_Source = row
			PAC_other = model.PAC_other(Cycle=PAC_other_Cycle, 
										FECRecNo=PAC_other_FECRecNo, 
										Filerid=PAC_other_Filerid, 
										# ContribLendTrans=PAC_other_ContribLendTrans,
										City=PAC_other_City, 
										State=PAC_other_State, 
										ZIP=PAC_other_ZIP, 
										FECOccEmp=PAC_other_FECOccEmp,
										PrimCode=PAC_other_Primcode, 
										Date=PAC_other_Date, 
										Amount=PAC_other_Amount, 
										RecipID=PAC_other_RecipID, 
										Party=PAC_other_Party, 
										Otherid=PAC_other_Otherid, 
										RecipCode=PAC_other_RecipCode,
										PrimCode=PAC_other_RecipPrimcode,
										# Amend=PAC_other_Amend, 
										# Report=PAC_other_Report, 
										# PG=PAC_other_PG, 
										# Microfilm=PAC_other_Microfilm, 
										# Type=PAC_other_Type, 
										RealCode=PAC_other_RealCode,
										# Source=PAC_other_Source)

