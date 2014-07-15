import MySQLdb
class DBContext( object ):
      def __init__(self):
         print "Init DBContext"
    	 self.db = MySQLdb.connect("localhost","prem1980","django","onlineshop" )
    	 #cursor = db.cursor()
             #sql = " insert into Products values (1,'name','slug','authorname',1,10.00,20.00,'Y','Y','Y','DESCRIPTION','META','META','2008-01-01 00:00:00','2008-01-01 00:00:01','IMAGE','THUMBNAIL','IMAGE')"
         #sql = " insert into Products values (2, 'End Times\xa0', '', 'Hardcover by Anna Schumacher', 10001, '13.49', '17.99', 'Y', 'Y', 'Y', 'Carbon County, Wyoming is like a current running through Daphne\x92s heart.When life gets too tough to bear in Detroit, Daphne flees to her Uncle Floyd\x92s home, where she believes she\x92ll find solace in the silent hills of her childhood summers. But Daphne\x92s Greyhound bus pulls over in downtown Carbon County and it\x92s not silence that welcomes her. It\x92s the sound of trumpets.', 'teen book', 'Teen & Young Adult', '2014-06-01 05:33:19', '2014-06-01 05:33:19', '', '', '10001_books.jpg')"
    	 #sql = "INSERT INTO Products values ( 3 , 'End Times' , '' , 'Hardcover by Anna Schumacher' , 10004 , '13.49' , '17.99' , 'Y' , 'Y' , 'Y' , 'Carbon County, Wyoming is like a current running through Daphnes heart.When life gets too tough to bear in Detroit, Daphne flees to her Uncle Floyds home, where she believes shell find solace in the silent hills of her childhood summers. But Daphnes Greyhound bus pulls over in downtown Carbon County and its not silence that welcomes her. Its the sound of trumpets.' , 'teen book' ,'Teen & Young Adult' , '2014-06-01 06:05:37' , '2014-06-01 06:05:37' , '' , '' , '10001_books.jpg')"
    	 #cursor.execute(sql)
         #db.commit()
         #print 'Insert over'

      def executequery(self,qry):
          print " In dbcontext execute query"
          self.cursor = self.db.cursor()
          try:
              self.cursor.execute(qry)
          except MySQLdb.Error as e:
              print "Error executing query ", qry
              
          results = self.dict_gen(self.cursor)
          
          #for row in results:
          #    print 'row =', row
          self.db.commit
          #for each in results:
          #    print 'each-1 =', each
          return results
    
      def dict_gen(self,curs):
          import itertools
          field_names = [d[0].lower() for d in curs.description]
          while True:
              rows = curs.fetchmany()
              if not rows: return
              for row in rows:
                yield dict(itertools.izip(field_names, row))
                
      def close(self):
          self.db.close()

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

#from django.utils import simplejson

#import json
#x = DBContext()
#result = x.executequery("Select id,name,author_name,price,old_price,description, image_caption from Products")
#to_json = []
#for each in result:
#print 'to_json = ', to_json    
    

#json_response = json.dumps(to_json, default = decimal_default)

