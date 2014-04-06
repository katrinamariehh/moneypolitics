
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text

import os
import model

from sys import argv

engine = create_engine(os.environ.get("DATABASE_URL"))
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush=False))

def house_funding(vote_id, cycle1, cycle2, catcode_start):
	voters = session.execute(
		text('''SELECT l.opensecrets_id, v.vote_value
				FROM legislators l 
				JOIN legislator_bill_house_votes v 
				ON (v.bioguide_id = l.bioguide_id) 
				WHERE v.vote_id = :vote_id'''),
			{'vote_id': vote_id})
	
	voter_funding_dict = {'Yea': [], 
						  'Nay': [],
						  'Aye': [],
						  'No': [],
						  'Present': [],
						  'Not Voting': []}

	for opensecrets_id in voters:
		pacs = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM pacs p
					WHERE cid = :opensecrets_id
					AND (cycle = :cycle1 or cycle = :cycle2)
					AND real_code LIKE :catcode_start
					GROUP BY real_code'''),
				{'opensecrets_id': opensecrets_id[0],
				 'cycle1': cycle1,
				 'cycle2': cycle2,
				 'catcode_start': catcode_start}
				 )
		pacothers = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM pacother
					WHERE recip_id = :opensecrets_id
					AND (cycle = :cycle1 or cycle = :cycle2)
					AND prim_code LIKE :catcode_start
					GROUP BY prim_code'''),
				{'opensecrets_id': opensecrets_id[0],
				 'cycle1': cycle1,
				 'cycle2': cycle2,
				 'catcode_start': catcode_start}
				 )
		individuals = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM individuals
					WHERE recip_id = :opensecrets_id
					AND (cycle = :cycle1 or cycle = :cycle2)
					AND real_code LIKE :catcode_start
					GROUP BY real_code'''),
				{'opensecrets_id': opensecrets_id[0],
				 'cycle1': cycle1,
				 'cycle2': cycle2,
				 'catcode_start': catcode_start}
				 )

		total = 0

		pacs = list(pacs)
		for pac in pacs:
			total += pac[0]

		pacothers = list(pacothers)
		for pacother in pacothers:
			total += pacother[0]

		individuals = list(individuals)
		for individual in individuals:
			total += individual[0]

		# voter_funding_dict[opensecrets_id[1]][opensecrets_id[0]] = total


		voter_dict = {}
		voter_dict['name'] = opensecrets_id[0]
		voter_dict['size'] = total

		voter_funding_dict[opensecrets_id[1]].append(voter_dict)


	keys = voter_funding_dict.keys()
	for key in keys:
		if voter_funding_dict[key] == {}:
			voter_funding_dict.pop(key)


	return voter_funding_dict


def senate_funding(vote_id, cycle1, cycle2, cycle3, catcode_start):
	voters = session.execute(
		text('''SELECT l.opensecrets_id, v.vote_value
				FROM legislators l 
				JOIN legislator_bill_senate_votes v 
				ON (v.lis_id = l.lis_id) 
				WHERE v.vote_id = :vote_id'''),
			{'vote_id': vote_id})
	
	voter_funding_dict = {'Yea': {}, 
						  'Nay': {},
						  'Aye': {},
						  'No': {},
						  'Present': {},
						  'Not Voting': {}}

	for opensecrets_id in voters:
		pacs = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM pacs p
					WHERE cid = :opensecrets_id
					AND (cycle = :cycle1 or cycle = :cycle2 or cycle = :cycle3)
					AND real_code LIKE :catcode_start
					GROUP BY real_code'''),
				{'opensecrets_id': opensecrets_id[0],
				 'cycle1': cycle1,
				 'cycle2': cycle2,
				 'cycle3': cycle3,
				 'catcode_start': catcode_start}
				 )
		pacothers = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM pacother
					WHERE recip_id = :opensecrets_id
					AND (cycle = :cycle1 or cycle = :cycle2 or cycle = :cycle3)
					AND prim_code LIKE :catcode_start
					GROUP BY prim_code'''),
				{'opensecrets_id': opensecrets_id[0],
				 'cycle1': cycle1,
				 'cycle2': cycle2,
				 'cycle3': cycle3,
				 'catcode_start': catcode_start}
				 )
		individuals = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM individuals
					WHERE recip_id = :opensecrets_id
					AND (cycle = :cycle1 or cycle = :cycle2 or cycle = :cycle3)
					AND real_code LIKE :catcode_start
					GROUP BY real_code'''),
				{'opensecrets_id': opensecrets_id[0],
				 'cycle1': cycle1,
				 'cycle2': cycle2,
				 'cycle3': cycle3,
				 'catcode_start': catcode_start}
				 )

		total = 0

		pacs = list(pacs)
		for pac in pacs:
			total += pac[0]

		pacothers = list(pacothers)
		for pacother in pacothers:
			total += pacother[0]

		individuals = list(individuals)
		for individual in individuals:
			total += individual[0]


		voter_funding_dict[opensecrets_id[1]][opensecrets_id[0]] = total

		keys = voter_funding_dict.keys()

	for key in keys:
		if voter_funding_dict[key] == {}:
			voter_funding_dict.pop(key)


	return voter_funding_dict

d = {'house_funding': house_funding,
	 'senate_funding': senate_funding}
