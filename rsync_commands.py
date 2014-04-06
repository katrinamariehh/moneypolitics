
for i in range(106, 114) :
	command = "rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/" + str(i) + "/votes " + str(i) + " &"
	print command

for i in range(106, 114) :
	command = "rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/" + str(i) + "/bills " + str(i) + " &"
	print command
