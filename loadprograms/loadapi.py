import csv
import sys
import MySQLdb
#import dbcontext
from datetime import datetime
import time    
ts = time.strftime('%Y-%m-%d %H:%M:%S')
created_at = datetime.now()
#db = DBContext()
db = MySQLdb.connect("localhost","prem1980","django","onlineshop" )

cursor = db.cursor()
cursor.execute("delete from onlineshop.Products")
i = 0
with open("data/Products.csv",'rb') as csvfile:
	spamreader = csv.reader(csvfile,delimiter=",")
	for row in spamreader:
                if i in [0]:
 		   pass
		else:
			#created_at and updated_at are set to current timestamp
 			row[0] = int(row[0])
 			row[4] = int(row[4])
			row[14] = row[13] = ts
			row[10] = row[10].replace('"','\\"')
			row[1] = row[1].replace('"','\\"')
			row[11] = row[11].replace('"','\\"')
			row[12] = row[12].replace('"','\\"')
			row[10] = row[10].decode('unicode_escape').encode('ascii','ignore')
			row[1] = row[1].decode('unicode_escape').encode('ascii','ignore')
			row[11] = row[11].decode('unicode_escape').encode('ascii','ignore')
			row[12] = row[12].decode('unicode_escape').encode('ascii','ignore')
			var_string = ', '.join('?' * len(row))
			print row
 			#Mysqldb does not allow parameterizzed query-- you can check using import MySQLdb and print MySQLdb.paramstyle
			#sql = '''INSERT INTO Products VALUES ({0})'''.format(var_string)
		        #sql = " insert into Products values (1,'name','slug','authorname',1,10.00,20.00,'Y','Y','Y','DESCRIPTION','META','META','2008-01-01 00:00:00','2008-01-01 00:00:01','IMAGE','THUMBNAIL','IMAGE')"
			x = 0 
			output = ' '
			for each in row:
				if x in [0,4]:
					output = output + str(each) + ' , '		
				else:
					output = output + '"' + str(each) + '"' +  ' , '
				x += 1
		#		print 'output =', output
			output = output[:-2]
                        print 'len of row =', len(output)
			sql = "INSERT INTO Products values (%s)" % output
			print 'sql =', sql
			#try:
			cursor.execute(sql)
			db.commit()
			#except Exception, e:
			#    print "Error %s" % (e.args[0])
			#    sys.exit(1)
		i += 1

                
              
