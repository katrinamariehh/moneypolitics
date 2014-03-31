# queries to pull data from moneypolitics
# visualizations of said data
# functions to pull data on specific individuals

select legislators.first_name, legislators.last_name, legislator_bill_votes.vote_value 
	from (legislators join legislator_bill_votes on 
		legislator_bill_votes.legislator_id = legislators.lis_id) where vote_id = 's396-111.2009';


select legislators.first_name, legislators.last_name, sum(individuals.amount) from (legislators join individuals on individuals.recip_id = legislators.opensecrets_id) where individuals.real_code like 'H%' and cycle = 2008 group by legislators.first_name, legislators.last_name;