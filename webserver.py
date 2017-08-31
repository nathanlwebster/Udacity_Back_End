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
                output += "<a href='#'>Edit</a>"
                output += "</br>"
                output += "<a href='#'>Delete</a>"
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
                self.send_header('Content-type',    'text/html')
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