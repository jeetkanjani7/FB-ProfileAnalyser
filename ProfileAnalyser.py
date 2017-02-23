import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
import facebook
import sqlite3
import csv


def get_commentscount(comments):
	count=0
	for com in comments['data']:
		count+=1
	return count
def get_ReactionsCount(reacts):
	r = ['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY']
	rno=[0] * 6
	for react in reacts['data']:
		index=r.index(react['type'])
		rno[index]+=1	
	return rno	

def update_reactions(reacts):
	

	#picture_count+=1
	rno = get_ReactionsCount(reacts)
	
	
	#if(rno[0]>max_likes):
	#	max_likes=picture_count
	#if(rno[1]>max_loves):
	#	max_loves=picture_count
	#if(rno[3]>max_wow):
	#	max_wow=picture_count
	#print("likes: "+ str(rno[0])+ "loves: "+ str(rno[1])+ "Haha: "+ str(rno[2])+ "WOW: "+ str(rno[3])+ "Sad: "+ str(rno[4])+ "Angry: "+ str(rno[5]))
	#print("\ncomments: "+str(comno))
	#print(reacts['summary'])
	return rno


def update_comments(comments):
	comno=get_commentscount(comments)
	return comno


def insert_into_db(profilepic):
	for dp in profilepic['data']:
		#print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
		print("\n")
		time=graph.get_object(id=dp['id'],fields="created_time")
		reacts=graph.get_object(id=dp['id']+'/reactions',limit=400,field='type')
		comments=graph.get_object(id=dp['id']+'/comments',limit=200,field='from')
		rno=update_reactions(reacts)
		cmno=update_comments(comments)
		#reacts=graph.get_object(id=dp['id'],fields='reactions.type(LIKE).summary(total_count).limit(0).as(like),reactions.type(LOVE).summary(total_count).limit(0).as(love),reactions.type(WOW).summary(total_count).limit(0).as(wow),reactions.type(HAHA).summary(total_count).limit(0).as(haha),reactions.type(SAD).summary(total_count).limit(0).as(sad),reactions.type(ANGRY).summary(total_count).limit(0).as(angry)')
		#for react in reacts:
			#print(react)
			#print(react['summary']['total_count'])
	
		
		pid=dp['id']
		try:	
			if(dp['name']):
				print( time["created_time"].split("T")[0]+"    "+dp['name'])	
				pname=dp['name']

		except KeyError:
			print(time["created_time"].split("T")[0]+"    "+"Caption not present")
			pname="Caption not present"
				
		params = (pid,pname,cmno,rno[0],rno[1],rno[3],time["created_time"].split("T")[0])
		c.execute("INSERT OR IGNORE INTO pictures VALUES(?,?,?,?,?,?,?)",params)
		
	max_likes=c.execute("select MAX(likes) as max_likes,caption,cdate from pictures")
	for r1 in max_likes:
		print("\n------------------------------------------------------------------------------------------------------------------------------------")
		print(" Most liked picture: "+str(r1[1])+"\n date= "+str(r1[2])+"\n likes= "+str(r1[0]))
		print("------------------------------------------------------------------------------------------------------------------------------------")
	max_loves=c.execute("select MAX(loves) as max_loves,caption,cdate from pictures")
	for r2 in max_loves:
		print("\n------------------------------------------------------------------------------------------------------------------------------------")
		print(" Most loved picture: "+str(r2[1])+"\n date= "+str(r2[2])+"\n loves= "+str(r2[0]))
		print("------------------------------------------------------------------------------------------------------------------------------------")
	max_comments=c.execute("select MAX(comments) as max_comments,caption,cdate from pictures")
	for r3 in max_comments:
		print("\n------------------------------------------------------------------------------------------------------------------------------------")
		print(" Most commented picture: "+str(r3[1])+"\n date= "+str(r3[2])+"\n comments= "+str(r3[0]))	
		print("------------------------------------------------------------------------------------------------------------------------------------")
	max_wows=c.execute("select MAX(wows) as max_wows,caption,cdate from pictures")
	for r4 in max_wows:
		print("\n------------------------------------------------------------------------------------------------------------------------------------")
		print(" Most wowed picture: "+str(r4[1])+"\n date= "+str(r4[2])+"\n wowed= "+str(r4[0]))	
		print("------------------------------------------------------------------------------------------------------------------------------------")

def perform_analysis(username, albums):
	for a in albums['data']:
		if(a['name']=="Profile Pictures"):
			profilepic=graph.get_object(id=a['id']+'/photos',field='name')
			profilepic['data'] = filter(None, profilepic['data'])
			insert_into_db(profilepic)


	


	with open('pictures.csv', 'w') as f:
		writer = csv.writer(f, delimiter=',')
		#for row in c.execute("SELECT * FROM pictures"):	
		#	row= [text.encode("utf8") for text in row]
		#	writer.writerow(row)

			#print(row)
			#print(type(row))
			#writer.write("hello\n")
	f.close()		
	print("users pictures inserted in pictures.csv")

if __name__ == '__main__':

	

	graph=facebook.GraphAPI(access_token="EAACEdEose0cBAAz3DrmdzO8lV6OlrXnZCwXYNWRljx7LNyDtwIYfCyhUh2kE8QOqz2FSqu9WMgmdlSnCDRj59zynF70tNuLnk5Dki9H5kQtmj19YubZChiIx12EH37kZCwX2MWK5jQdxpvcj6pyffcZAZAZB1M1bPBbwtcBNXZCfZCKZB9nHOpdJeULDt3MNyijIZD", version=2.8)
	albums=graph.get_object(id='me/albums', field='name')
	me=graph.get_object(id='me')

	db_name = str(me['name'] + '_' + "profile")
	conn = sqlite3.connect(db_name[:-1])
	c = conn.cursor()
	c.execute("DROP TABLE IF EXISTS pictures")
	c.execute('''CREATE TABLE IF NOT EXISTS pictures
	(PictureID TEXT PRIMARY KEY NOT NULL,
	 caption TEXT NOT NULL,
	 comments INTEGER,
	 likes INTEGER,
	 loves INTEGER,
	  wows INTEGER,
	  cdate TEXT)
	''')
	
	perform_analysis(me['name'],albums) 



	conn.commit()
	conn.close()
