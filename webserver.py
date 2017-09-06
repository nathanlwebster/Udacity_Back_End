from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):
            print("troubleshooting")
            restaurants = session.query(Restaurant).all()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<a href='/restaurants/new'>Create a new restaurant</a>"
            output += "</br>"
            output += "</br>"

            for restaurant in restaurants:
                output += restaurant.name
                output += "</br>"
                output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                output += "</br>"
                output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                output += "</br>"
                output += "</br>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return
        
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<form method='POST' action='/restaurants/new' enctype='multipart/form-data'><h2>New restaurant name:</h2>"
            output += "<input name='newRestaurantName' type='text' ><input type='submit' value='Submit'> </form>"
            output += "</body></html>"
            self.wfile.write(output)
            return
        
        if self.path.endswith("/edit"):
            restaurantIDPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
            if myRestaurantQuery != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>"
                output += myRestaurantQuery.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit' >" % restaurantIDPath
                output += "<input name='newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                output += "<input type='submit' value='Rename'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

        if self.path.endswith("/delete"):
            restaurantIDPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
            if myRestaurantQuery != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>"
                output += "Are you sure you want to delete %?" % myRestaurantQuery.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete' >" % restaurantIDPath
                output += "<input type='submit' value='Delete'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

        except:
            pass

        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]
                
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent[0]
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return

        except:
            pass

        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    restaurantIDPath = self.path.split("/")[2]
                
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()