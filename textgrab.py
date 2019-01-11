from bs4 import BeautifulSoup
import os
import urllib
import requests
import pymysql
import time


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

def handleTags(text):
	result = ''

	i = 0
	while i < len(text):
		if text[i] is '>' and text[i+1] is '>':
			#print text[i: i + 11]
			result = result + '\n' + text[i: i + 11 ] + ' '
			i = i + 11
		else:
			result = result + text[i]
			i = i + 1

	return result

def collectBoards():
	#collects boards from 4chan header
	#thia could probably be its own program; running it every time is inefficient
	r  = requests.get("http://4chan.org/")
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')
	boards = {}

															
	for span in soup.find_all('a', {"class": "boardlink"}):
		if(len(span) >= 1):
			boards[span.text] = ["https:" + span.get('href'), span.get('href')[ span.get('href').index('/',3) :]]	


	return boards, soup

def publish(dict, connection):
	#Used to insert collected posts/replies to SQL server
	#Input: replyDict/postDict
	try:
		try:
			if(dict.has_key('op_id')):
				#if a dictionary has the key 'op_id' then it is a reply
				#posts do not have an op_id since they are the OP					
				query = ("INSERT INTO `reply`(`reply_ID`, `op_id`,`dateTime`, `handle`, `subject`, `text`, `board`) VALUES (%s,%s,%s,%s,%s,%s,%s)")
				connection.cursor().execute(query, ( dict['reply_id'], dict['op_id'], dict['dateTime'], dict['handle'], dict['sub'], dict['text'], dict['board'] ))
				connection.commit()
				print dict['board'], dict['reply_id'], dict['op_id'], dict['dateTime'], dict['handle'], dict['sub'], type(dict['text']), dict['text']
			else:
				query = ("INSERT INTO `post`(`id`,`dateTime`, `text`, `handle`, `subject`, `board`) VALUES (%s,%s,%s,%s,%s,%s)")
				connection.cursor().execute( query, (dict['id'], dict['dateTime'], dict['text'],dict['handle'], dict['sub'], dict['board'] ) )
				onnection.commit()
				print dict['board'], dict['id'], dict['dateTime'], dict['text'],dict['handle'], dict['sub'], type(dict['board']), dict['text']
		
		except pymysql.err.IntegrityError:
			raise
	except:
		return


def scrape(boards, connection, soup, board_specific = ""):
	postDict = {'id': '','text': '','dateTime': '', 'handle': '', 'sub': '', 'board': ''}
	replyDict = {'text': '','dateTime': '', 'handle': '','sub':'', 'op_id': '', 'reply_id': ''}

	for key in boards:					#traverse boards	-main functionize // args: boards list, connection, soup
	# 	print key + "\t" + boards[key][1]	#print boards dict

		if(board_specific is not ""):

			if(boards[key][1] == board_specific):	#specify target board(s)
				r = requests.get(boards[key][0])
				data = r.text
				soup = BeautifulSoup(data, 'html.parser')
				
		else:
			break;
			# r = requests.get(boards[key][0])	#scrapes all boards
			# data = r.text
			# soup = BeautifulSoup(data, 'html.parser')
		
		replylink_list = [];
		for link in soup.find_all('a', {"class": "replylink"}):
			replylink = boards[key][0] + link.get('href')
			
			
			#post id length changes depending on the board
			#consider using some sort of regex
			if(replylink[:42] not in replylink_list):	#modify for thread updates - this condition controls for duplicate links
				replylink_list.append(replylink[:42])

				r_replylink = requests.get(replylink)
				data_replylink = r_replylink.text
				soup_replylink = BeautifulSoup(data_replylink, 'html.parser')


				#This loop handles posts in the format: id - text - dateTime - handle - subject - board
				for post in soup_replylink.find_all('div', {"class": "postContainer opContainer"}):

					#collects id
					try:
						postDict['id'] = id = replylink[replylink.index('/',30)+1:replylink.index('/',35)]
					except Exception as e:
						print e, 'at', replylink
						exit()

					#collects text
					replyDict['text'] = text = post.find('blockquote').text
					if '>>' in text:
						try:
							postDict['text'] = text = handleTags(str(text))
						except UnicodeEncodeError as e:
							continue


					#collects dateTime
					dateTime = post.find('span', {"class": "dateTime"}).text[:21]
					dateTime = dateConvert(dateTime)
					postDict['dateTime'] = dateTime

					# #collects handle
					postDict['hanlde'] = handle = post.find('span', {"class":"name"}).text, '\n'
					if(postDict['handle'] == ''):
						postDict['handle'] = 'Anonymous'

					# #collects subject
					sub = ""
					for subject in post.find_all('span', {"class": "subject"}):
						if(len(subject.text) ==  0):
							sub = "NoSubject"
						else:
							sub = subject.text
						
						postDict['sub'] = sub

					#collects board the post was on
					postDict['board'] = boards[key][1]
					try:
						if len(text) >= 3:
							publish(postDict, connection)
					except:
						continue
				"""
				future self
				capture filelinks
				"""

				##This loop handles replies in the format: text - dateTime - handle - subject - op_id - reply_id - board
				for reply in soup_replylink.find_all('div', {"class": "postContainer replyContainer"}):				
					#continue
					#print replylink, 'reply'
					
					#collects text
					replyDict['text'] = text = reply.find('blockquote').text
					if '>>' in text:
						try:
							replyDict['text'] = text = handleTags(str(text))
						except UnicodeEncodeError as e:
							continue

		
					#collects dateTime
					dateTime = reply.find('span', {"class": "dateTime"}).text[:21]
					replyDict['dateTime'] = dateTime = dateConvert(dateTime)


					#collects handle
					replyDict['handle'] = handle = reply.find('span', {"class":"name"}).text
					#empty handle check
					if(replyDict['handle'] == ''):
						replyDict['handle'] = 'Anonymous'

					# # #collects subject
					replyDict['sub'] = sub = ""
					for subject in reply.find_all('span', {"class": "subject"}):
						#empty subject check
						if(len(subject.text) ==  0):
							sub = "NoSubject"
						else:
							sub = subject.text
					replyDict['sub'] = sub

					#collects op_id
					replyDict['op_id'] = op_id = replylink[ replylink.index('/',30)+1 : replylink.index('/',35) ]


					#reply_id
					reply_id = -1
					for reply in reply.find_all('a', limit=1):
						reply_id = reply.get("href")[2:]
					replyDict['reply_id'] = reply_id

					#collects board the reply was on
					replyDict['board'] = boards[key][1]

					try:
						if len(text) >= 3:
							publish(replyDict, connection)
					except:
						continue
			else:
				continue

def main():
	#print handleTags('>>234356789>>789578121Of course. Only a fool would believe that shit happened')
	boards, soup = collectBoards()
	connection = connectToSQL()
	timer = time.time()
	# try:
	# 	while True:
	# 		scrape(boards, connection, soup, '/b/')
	# except:
	# 	print "Local Runtime: ", time.time() - timer, "seconds"
	# 	exit()
	
	while True:
		scrape(boards, connection, soup, '/b/')

if __name__ == "__main__":
	main()