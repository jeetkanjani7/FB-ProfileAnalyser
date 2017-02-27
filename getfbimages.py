import facebook
import urllib2
import requests as r

GRAPH_API_URL="https://graph.facebook.com/v2.8/"
if __name__ == '__main__':
	print("bhaag")
	with open('details.txt', 'r') as f:
		ACCESS_TOKEN=f.readline()
		U_ID=f.readline()
 	
	params={"access_token":ACCESS_TOKEN}
	resp = r.get(GRAPH_API_URL+"/me", params = params)

	OUTPUT_FILE = "fbscrape"

	params={"access_token":ACCESS_TOKEN, "fields":"images"}

	indexFile = open("index.csv", "r")

	for line in indexFile:
		parts = line.split(",")
		photoId = parts[0].strip()
		resp = r.get(GRAPH_API_URL+photoId, params=params)
		images = resp.json()["images"]
		imgUrl = ""
		for img in images:
			if img["width"] == 720:
				imgUrl = img["source"].encode("UTF-8")

		if imgUrl:
			imgUrlSplit = imgUrl.split("?")
			imgParams = {}
			if len(imgUrlSplit) > 1:
				imgUrl = imgUrlSplit[0]
				for param in imgUrlSplit[1].split("&"):
					p = param.split("=")
					key = p[0]
					value = p[1]
					imgParams[key] = value
			imageResp = r.get(imgUrl, params=imgParams);
			with open(OUTPUT_FILE+photoId+".jpg", "wb") as imageFile:
				imageResp.raw.decode_content = True
				imageFile.write(imageResp.content)




	indexFile.close()