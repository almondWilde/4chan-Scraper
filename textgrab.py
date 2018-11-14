from bs4 import BeautifulSoup
import os
import urllib
import requests

#testhtml = open('fortune.html', 'w')

r  = requests.get("http://4chan.org/")
data = r.text
soup = BeautifulSoup(data, 'html.parser')
boards = {}

#testhtml.write(data.encode('ascii', 'ignore'))			#output html to file
														
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
				#for post in soup_replylink.find_all('div', {"class": "postContainer opContainer"}):
					#print post,  '\n'

					#continue

					#collects id
					#print replylink[35:42]

					#collects text
					# for text in post.find_all('blockquote'):
					#  	print text.text

					#collects dateTime
					# print post.find('span', {"class": "dateTime"}).text[:21]

					# #collects handle
					# print post.find('span', {"class":"name"}).text, '\n'

					# #collects subject
					# for subject in post.find_all('span', {"class": "subject"}):
					# 	if(len(subject.text) ==  0):
					# 		print "no subject"
					# 	else:
					# 		print subject.text

				"""
				future armand
				filelinks

				also store board for each post in db
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