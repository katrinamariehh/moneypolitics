# rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/112/bills 112

# rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/[number]/bills [number] where number goes from 84-111

# 107, 110



for i in range(108, 114) :
	command = "rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/" + str(i) + "/votes " + str(i) + " &"
	print command

for i in range(108, 114) :
	command = "rsync -avz --delete --delete-excluded --exclude **/text-versions/ govtrack.us::govtrackdata/congress/" + str(i) + "/bills " + str(i) + " &"
	print command
