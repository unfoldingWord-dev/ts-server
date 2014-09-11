Translation Studio Server
---

This repository contains the server side code for interacting with the Translation Studio app.

###Environment
The server script uses the [Twisted] library to create a web service that handles requests from the mobile app.

###Testing
To test on your local environment you'll need a tool that can communicate with a tcp port such as telnet.
Telnet is available on OSX by default, but you'll need to 
[manually enable telnet](http://technet.microsoft.com/en-us/library/cc771275(v=ws.10).aspx) it if using Windows 7.

># connect to the port
>telnet 127.0.0.1 [port]
># send a message
>hello world

[Twisted]:https://twistedmatrix.com/trac/