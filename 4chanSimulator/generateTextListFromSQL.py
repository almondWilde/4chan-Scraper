import pymysql

def connectToSQL():
	#connects to SQL Server
	#alter credentials accordingly
	HOST = "localhost"
	USER = "root"
	DB = "Community"
	connection = pymysql.connect(host = HOST, user = USER, db = DB, cursorclass=pymysql.cursors.DictCursor)

	return connection

# def printToFile(file, string):

def main():
	outFile = open('out.dat', 'w')
	connection = connectToSQL();
	cursor = connection.cursor()
	print 'a'
	#query = ("SELECT `post`.`text`, `reply`.`text` FROM `post`, `reply` WHERE `post`.`text` <> '' AND `reply`.`text` <> '' ")
	query = ("SELECT `reply`.`text` FROM `reply` WHERE `reply`.`text` <> '' ")
	print 'a'
	cursor.execute(query)
	print 'a'
	rows = cursor.fetchall()		#rows is a lst of dicts {text: [post.reply, reply.reply}
	

	for d in rows:
			outFile.write(d.values()[0] + '\n' )
			

if __name__ == "__main__":
	main()