from bs4 import BeautifulSoup
import os
import urllib
import requests

#testhtml = open('fortune.html', 'w')

r  = requests.get("http://4chan.org/")
data = r.text
soup = BeautifulSoup(data, 'html.parser')
boards = {}

#print "here"
#testhtml.write(data.encode('ascii', 'ignore'))			#output html to file
														
for span in soup.find_all('a', {"class": "boardlink"}):	#capture board names
	#print span
	#print len(span)
	if(len(span) >= 1):
		boards[span.text] = "https:" + span.get('href')	

# for key in boards:					#for each board in boards	
#  	#print key + "\t" + boards[key]	#print boards dict
 	
# 	# try:
# 	# 	os.mkdir(key)
# 	# except (OSError):
# 	# 	continue

key = "Random"
r = requests.get(boards[key])					#change boards[key] to a thread link if you want to capture all the images in a thread
data = r.text
soup = BeautifulSoup(data, 'html.parser')

#print soup.find_all('img')						#list of all images
#if you wanted to look through every image in every thread then you must:
#	1. nest the below for loop inside another for loop where:
#		a. for reply link in soup.find_all(('a', {"class": "boardlink"}))
#		b. use the request, data, soup pattern above

for img in soup.find_all('img'):
	#print img
	image_url = "http:" + img.get('src')		#this method does not work with GIFS
	image_url = image_url.replace('s', '')			#preview image names end in ...s.jpg
												#to get originals the s at the end must be removed
	print image_url

	try:
		image_name = os.path.split(image_url)[1]			    	
		filepath = key + '/' + image_name
		#print filepath
		urllib.urlretrieve(image_url, os.path.basename(image_name))
	except(IOError):							#banners send an IOError becasue their urls start with s.4cdn.org...
												#in order to fix the preview problem the s in banner urls are removed causing IOError
												#this IOError also catches
		continue
