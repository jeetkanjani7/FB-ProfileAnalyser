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
	

	
	rno = get_ReactionsCount(reacts)
	
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
		print(" Most wowed picture: "+str(r4[1])+"\n date= "+str(r4[2])+"\n wows= "+str(r4[0]))	
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

	with open('details.txt', 'r') as f:
		ACCESS_TOKEN=f.readline()
		U_ID=f.readline()

    
	graph = facebook.GraphAPI(ACCESS_TOKEN, version='2.8')
	user=graph.get_object(id=U_ID)
	albums=graph.get_object(id=U_ID+'/albums', field='name')
	

	db_name = str(user['name'] + '_' + "profile")
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
	
	perform_analysis(user['name'],albums) 



	conn.commit()
	conn.close()
