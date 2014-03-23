import os

def create_finance_list(path):
	# create paths for reading in Campaign Finance documents
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
# divide the path_list into lists based on the type
# each type gets fed into a different function in the seed script

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
	# create a path list for the congressional records
	path_list = []
	contents = os.listdir(path)
	# skip the follwoing nodes--they are less important bills, links to text files, etc.
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

# create an empty dictionary to add votes and bills as different separate lists 
# which will be fed to different functions in the seed
cpaths = {}


def parse_congress_list(list):
# instantiate the empty values in the dictionary
	cpaths['votes'] = []
	cpaths['bills'] = []

	for path in list:
		# add the path to either votes or bills based on which one appears  in the path string
		if 'votes' in path:
			cpaths['votes'].append(path)
		if 'bills' in path:
			cpaths['bills'].append(path)

	return cpaths

def main():

	CampaignFin_list = create_finance_list('data/CampaignFin')
	CampaignFin_paths = parse_finance_list(CampaignFin_list)

	congress_list = create_congress_list('data/congress')
	congress_paths = parse_congress_list(congress_list)

if __name__ == "__main__":
	main()






