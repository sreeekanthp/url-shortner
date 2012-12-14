import webapp2
import random
import cgi
from google.appengine.ext import db

class data(db.Model):
	longurl=db.StringProperty(multiline=True)
	shorturl=db.StringProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
          	<html>
            	<body>
		
		<center>
		<font size="30"color = "red">URL SHORTENER</font>
		<br><br><br><br><br>
              	<form >
                <div><textarea name="content" rows="3" cols="60"></textarea></div>
                <div><input type="submit" value="ShortUrl"></div>
              	</form></center>""")
		longurl=self.request.get('content')
		l = len(longurl)
		val1=[]
		#val1.append("/")
		for i in range(0,l-1):
			#s=0
			#s = ord(longurl[i])
			#s = str(s)
			if i%7==0:
				val1.append(longurl[i])
				#val1.append("'")
		shorturl = ''.join(val1)
		if longurl != "":
			obj=data(db.Key.from_path('URL',longurl))
			#self.response.out.write(store.longurl)
			obj.longurl=longurl
			obj.shorturl=shorturl
			#self.response.out.write(longurl)
			url=db.GqlQuery("SELECT * FROM data WHERE ANCESTOR IS :c",c=db.Key.from_path('URL',longurl))
			count =0
			for i in url:
				count=count+1
			if count==0:
				obj.put()
			short=self.request.path[1:]
			url1=db.GqlQuery("SELECT * FROM data WHERE ANCESTOR IS :c",c=db.Key.from_path('URL',longurl))
			
			for i in url1:
				self.response.out.write("<center><br/><br/>Shortened Url")
				self.response.out.write('<center><font color="green">')
				self.response.out.write('sreekanthshort.appspot.com/')
				self.response.out.write(i.shorturl)
				self.response.out.write('</font></center>')
				self.response.out.write("""<br></center>""")
			self.response.out.write("""</body></html>""")
		if self.request.path[1:]!="":
			dat=data.all()
			obj1 = dat.filter("shorturl =",self.request.path[1:]).get()
			self.redirect(str(obj1.longurl))			

app=webapp2.WSGIApplication([('/.*',MainPage)],debug=True)		
