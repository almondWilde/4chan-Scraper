# textGrab
4chan Web Scraper usiing BeautifulSoup

Requires an SQL server hosting "Community.sql" at localhost as the root user.

Default credentials:
	HOST: localhost
	DATABASE: Community.sql
	USER: root

These credentials can be changed in the connectToSQL().
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Instsallation:
	pip install requirements.txt
Run:
	python textGrab.py

Output:


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Future:
	Handle various boards of different tag lengths (i.e. /pol/, /b/)
		-choose board from terminal