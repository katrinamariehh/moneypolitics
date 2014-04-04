from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy.sql import text
from sqlalchemy import func
from operator import itemgetter
import os
import model

engine = create_engine(os.environ.get("DATABASE_URL"))
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush=False))

def house_funding(vote_id):
	voters = session.execute(
		text('''SELECT l.opensecrets_id, v.vote_value
				FROM legislators l 
				JOIN legislator_bill_house_votes v 
				ON (v.bioguide_id = l.bioguide_id) 
				WHERE v.vote_id = :vote_id'''),
			{'vote_id': vote_id})
	
	voter_funding_dict = {'Yea': {}, 'Nay': {}}

	for opensecrets_id in voters:
		pacs = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM pacs p
					WHERE cid = :opensecrets_id
					AND (cycle = 2006 or cycle=2008)
					AND real_code LIKE 'F%'
					GROUP BY real_code'''),
				{'opensecrets_id': opensecrets_id[0]})
		pacothers = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM pacother
					WHERE recip_id = :opensecrets_id
					AND (cycle = 2006 or cycle=2008)
					AND prim_code LIKE 'F%'
					GROUP BY prim_code'''),
				{'opensecrets_id': opensecrets_id[0]})
		individuals = session.execute(
			text('''SELECT sum(amount) AS sum_amount
					FROM individuals
					WHERE recip_id = :opensecrets_id
					AND (cycle = 2006 or cycle=2008)
					AND real_code LIKE 'F%'
					GROUP BY real_code'''),
				{'opensecrets_id': opensecrets_id[0]})

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

	return voter_funding_dict




				# h681-110.2008