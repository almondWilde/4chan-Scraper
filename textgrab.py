from bs4 import BeautifulSoup
import os
import urllib
import requests
import pymysql

def dateConvert(date4):	#converts 4chan dateTime format to mysql
	#mo/da/yr(day_abr)hh:mm:ss => yyyy-mm-ss hh:mm:ss
	mdate = "20" + date4[6:8] + '-' + date4[:2] + '-' + date4[3:5] + ' ' +date4[date4.index(')')+1:]
	return mdate

#print dateConvert("11/20/18(Tue)16:47:00")

#for pymysql
HOST = "localhost"
USER = "root"
DB = "Community"
connection = pymysql.connect(host = HOST, user = USER, db = DB, cursorclass=pymysql.cursors.DictCursor)
print type(connection)

# connection.cursor().execute("INSERT INTO `post`(`id`,`dateTime`, `text`, `handle`, `subject`, 'board') VALUES (\"12:12:12\",\"12345673\",\"textSampe asdf\",\"anon\",\"subject test\", \"/b/\")")
# connection.commit()

r  = requests.get("http://4chan.org/")
data = r.text
soup = BeautifulSoup(data, 'html.parser')
boards = {}

														
for span in soup.find_all('a', {"class": "boardlink"}):	#capture board names
	# print span
	# print len(span)
	if(len(span) >= 1):
		boards[span.text] = ["https:" + span.get('href'), span.get('href')[18:]]	

for key in boards:					#for each board in boards	
# 	print key + "\t" + boards[key][1]	#print boards dict

	if(boards[key][1] == "/b/"):
		r = requests.get(boards[key][0])
		data = r.text
		soup = BeautifulSoup(data, 'html.parser')

		replylink_list = [];
		for link in soup.find_all('a', {"class": "replylink"}):
			replylink = "http://boards.4chan.org" + boards[key][1] + link.get('href')
			
			#post number size changes depending on the board
			#consider using some sort of regex
			if(replylink[:35] not in replylink_list):
				replylink_list.append(replylink[:35])

				r_replylink = requests.get(replylink)
				data_replylink = r_replylink.text
				soup_replylink = BeautifulSoup(data_replylink, 'html.parser')

#				
				# print len(replylink_list), replylink_list[len(replylink_list) - 1]

				print replylink
				#posts: text - dateTime - subject - fileLink - postID?
				for post in soup_replylink.find_all('div', {"class": "postContainer opContainer"}):
					#print post,  '\n'

					

					#collects id
					id = replylink[35:42]

					text = ""
					#collects text
					for body in post.find_all('blockquote'):
					 	text = body.text

					#collects dateTime
					dateTime = post.find('span', {"class": "dateTime"}).text[:21]
					dateTime = dateConvert(dateTime)

					# #collects handle
					handle= post.find('span', {"class":"name"}).text, '\n'

					# #collects subject
					sub = ""
					for subject in post.find_all('span', {"class": "subject"}):
						if(len(subject.text) ==  0):
							sub = "no subject"
						else:
							sub = subject.text

					print id, dateTime, text, handle[0], sub, boards[key][1]

					#check for dupliccate id's for updated posts; theres a way to handle it, just google it
					query = ("INSERT INTO `post`(`id`,`dateTime`, `text`, `handle`, `subject`, `board`) VALUES (%s,%s,%s,%s,%s, %s)")
					connection.cursor().execute(query, (id, dateTime, text,handle[0], sub, boards[key][1]))
					connection.commit()

				"""
				future self
				capture filelinks
				"""

				#replies: op - dateTime - text - name - file?
				for post in soup_replylink.find_all('div', {"class": "postContainer replyContainer"}):
					
					continue
					# #collects text
					# for text in post.find_all('blockquote'):
					#  	print text.text, '\n'
		
					# #collects dateTime
					# print post.find('span', {"class": "dateTime"}).text[:21]

					# # # #collects handle
					# print post.find('span', {"class":"name"}).text

					# # #collects subject
					# for subject in post.find_all('span', {"class": "subject"}):
					# 	print subject.text

					# #collects op_id
					# print replylink[33:42]

					# #reply_id
					# for reply in post.find_all('a', limit=1):
					# 	print reply.get("href")[2:]