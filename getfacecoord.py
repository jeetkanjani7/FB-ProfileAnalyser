import urllib2
import requests as r
import facebook

GRAPH_API_URL="https://graph.facebook.com/v2.8/"
if __name__ == '__main__':
	print("bhaag")
	with open('details.txt', 'r') as f:
		ACCESS_TOKEN=f.readline()
		U_ID=f.readline()
 	
	params={"access_token":ACCESS_TOKEN}
	resp = r.get(GRAPH_API_URL+"/me", params = params)
	
	USER_ID = resp.json()["id"]
	print(USER_ID)

	run = True
	after = None
	outFile = open("index.csv", "w")
	pages = 0
	
	while run and pages < 5: #hacked do while
		params={"access_token":ACCESS_TOKEN, "after":after}
		resp = r.get(GRAPH_API_URL+USER_ID+"/photos?type=tagged", params=params)
		data = resp.json()["data"]

		if "paging" in resp.json():	
			after = resp.json()["paging"]["cursors"]["after"]
		else:
			run = False

		pages+=1
	for photo in data:
		photoId = photo["id"]
		tagsParams = {"access_token":ACCESS_TOKEN}
		tagsResp = r.get(GRAPH_API_URL+photoId+"/tags", params=tagsParams)
		tagsData = tagsResp.json()["data"]
		for tag in tagsData:
				if (tag["name"] == "Jeet Kanjani"):
					x = tag["x"]
					y = tag["y"]
					print str(photoId) +"," +str(x)+","+str(y)
					outFile.write("{0}, {1}, {2}\n".format(photoId, x, y))