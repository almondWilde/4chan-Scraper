from bs4 import BeautifulSoup
import os
import urllib
import requests
import pymysql

def dateConvert(date4):	
	#converts 4chan dateTime format to mysql
	#Pre: mo/da/yr(day_abr)hh:mm:ss
	#Post: yyyy-mm-ss hh:mm:ss
	mdate = "20" + date4[6:8] + '-' + date4[:2] + '-' + date4[3:5] + ' ' +date4[date4.index(')')+1:]
	return mdate

def connectToSQL():
	#connects to SQL Server
	#alter credentials accordingly
	HOST = "localhost"
	USER = "root"
	DB = "Community"
	connection = pymysql.connect(host = HOST, user = USER, db = DB, cursorclass=pymysql.cursors.DictCursor)

	return connection

def collectBoards():
	#collects boards from 4chan header
	#thia could probably be its own program; running it every time is inefficient
	r  = requests.get("http://4chan.org/")
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')
	boards = {}

															
	for span in soup.find_all('a', {"class": "boardlink"}):
		if(len(span) >= 1):
			boards[span.text] = ["https:" + span.get('href'), span.get('href')[18:]]	

	return boards, soup


def main(boards, connection, soup, board_specific = "/b/"):
	for key in boards:					#traverse boards	-main functionize // args: boards list, connection, soup
	# 	print key + "\t" + boards[key][1]	#print boards dict


		if(boards[key][1] == "/b/"):	#specify target board(s)
			r = requests.get(boards[key][0])
			data = r.text
			soup = BeautifulSoup(data, 'html.parser')

			replylink_list = [];
			for link in soup.find_all('a', {"class": "replylink"}):
				replylink = "http://boards.4chan.org" + boards[key][1] + link.get('href')	#only scrapes the front page
				
				
				#post id length changes depending on the board
				#consider using some sort of regex
				if(replylink[:42] not in replylink_list):	#modify for thread updates - this condition controls for duplicate links
					replylink_list.append(replylink[:42])

					r_replylink = requests.get(replylink)
					data_replylink = r_replylink.text
					soup_replylink = BeautifulSoup(data_replylink, 'html.parser')


					#posts: id - text - dateTime - handle - subject - board
					for post in soup_replylink.find_all('div', {"class": "postContainer opContainer"}):
						#collects id

						#continue
						id = replylink[35:42]

						#collects text
						text = post.find('blockquote').text

						#collects dateTime
						dateTime = post.find('span', {"class": "dateTime"}).text[:21]
						dateTime = dateConvert(dateTime)

						# #collects handle
						handle = post.find('span', {"class":"name"}).text, '\n'

						# #collects subject
						sub = ""
						for subject in post.find_all('span', {"class": "subject"}):
							if(len(subject.text) ==  0):
								sub = "NoSubject"
							else:
								sub = subject.text

						print id, dateTime, text, handle[0], sub, boards[key][1]

						#check for dupliccate id's for updated posts; theres a way to handle it, just google it
						query = ("INSERT INTO `post`(`id`,`dateTime`, `text`, `handle`, `subject`, `board`) VALUES (%s,%s,%s,%s,%s, %s)")
						connection.cursor().execute(query, (id, dateTime, text,handle, sub, boards[key][1]))
						connection.commit()

					"""
					future self
					capture filelinks
					"""

					#replies: text - dateTime - handle - subject - op - id - board
					for post in soup_replylink.find_all('div', {"class": "postContainer replyContainer"}):				
						#continue
						#collects text
						text = post.find('blockquote').text
			
						#collects dateTime
						dateTime = post.find('span', {"class": "dateTime"}).text[:21]

						#collects handle
						handle = post.find('span', {"class":"name"}).text

						# # #collects subject
						sub = ""
						for subject in post.find_all('span', {"class": "subject"}):
							if(len(subject.text) ==  0):
								sub = "NoSubject"
							else:
								sub = subject.text

						#collects op_id
						op_id = replylink[33:42]

						#reply_id
						reply_id = -1
						for reply in post.find_all('a', limit=1):
							reply_id = reply.get("href")[2:]

						print reply_id, op_id, dateTime, text, handle[0], sub, boards[key][1]
						
						query = ("INSERT INTO `reply`(`reply_ID`, `op_id`,`dateTime`, `handle`, `subject`, `text`, `board`) VALUES (%s,%s,%s,%s,%s,%s,%s)")
						connection.cursor().execute(query, (reply_id, op_id, dateTime,handle, sub, text, boards[key][1]))
						connection.commit()



boards, soup = collectBoards()
connection = connectToSQL()

main(boards, connection, soup)