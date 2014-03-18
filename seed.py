# the Contrib field on the Indiv table is going to be problematic; there's a comma in the middle and it's delimited by pipes, so it'll be like ',|Hall-Hutzley, Katrina|,'--this will matter in the seed file when I'm loading my rows into my database
# with CSV reader, pipes may be quote characters--try this tomorrow reading in one CampaignFin14 file

# you can map a zip to a dictionary--use this for passing in headers

# xmltodict to parse the xml data in the people_legacy file to a dictionary to send into the database--I should be able to easily read dictionaries into the database, right?

# requests can make http requests for make 

# I think i need to just throw all of the votes and bills into a the database and start dealing with it