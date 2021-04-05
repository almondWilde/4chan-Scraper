# 4chan Scraper

4chan Web Scraper using BeautifulSoup

# Image Scraper

# Text Scraper
Requires an SQL server hosting "Community.sql" at localhost as the root user. Tested with XAMPP

 Default credentials:
	HOST: localhost
	DATABASE: Community.sql
	USER: root

These credentials can be changed in the connectToSQL().

Instsallation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	pip install -r requirements.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Run:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	python textGrab.py 			#for text with SQL Server
	python captureImagesFromWebsite.py 	#for image capturing; send thread link in terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
