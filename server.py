#  coding: utf-8 
import SocketServer
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


from os import curdir

class MyWebServer(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        requestArray = self.data.split()
        
        if(requestArray[0]=="GET"):
            try:
                if(requestArray[1] == "/"):
                    resultFile = open(curdir + "/www/index.html", "r").read()
                    mimeType = "text/html" 
                elif(requestArray[1].endswith("/")):
                    resultFile = open(curdir + "/www" + requestArray[1] + "index.html", "r").read()
                    mimeType = "text/html"
                elif(requestArray[1].endswith(".css")):
                    resultFile = open(curdir + "/www" + requestArray[1], "r").read()
                    mimeType = "text/css"
                
                elif(requestArray[1].endswith(".html")):
                    resultFile = open(curdir + "/www" + requestArray[1], "r").read()
                    mimeType = "text/html"
                else:
                    self.request.sendall("HTTP/1.1 404 Path Not Found \r\n")
                    return

                fileLength = len(resultFile)
                self.request.sendall("HTTP/1.1 200 OK \r\n" 
                    + "Content-Length: " + str(fileLength) + "\r\n" 
                    + "Content-Type: " + mimeType + "\r\n" 
                    + "Connection: close \r\n" + "\r\n" + resultFile)
            except IOError:
                self.request.sendall("HTTP/1.1 404 File Not Found \r\n");

        else:
            self.request.sendall("HTTP/1.1 405 Method Not Allowed \r\n")


        self.request.sendall("OK")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()