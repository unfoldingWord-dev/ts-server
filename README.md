Translation Studio Server
---

This repository contains the server side code for interacting with the Translation Studio app.

###Environment
The server script uses the [Twisted] library to create a web service that handles requests from the mobile app.

###Testing
To test on your local environment you'll need a tool that can communicate with a tcp port such as telnet.
Telnet is available on OSX by default, but you'll need to 
[manually enable telnet](http://technet.microsoft.com/en-us/library/cc771275(v=ws.10).aspx) it if using Windows 7.

>\# connect to the port (you may need to change the port)
>
>telnet 127.0.0.1 1234
>
>\# send a message
>
>hello world

###Usage
The script expects to receive json data `{'key':'public key', 'udid':'device id', 'username':'an optional username'}`  
where `key` is the public ssh key of the mobile device, `udid` is the unique device id and the optional`usename` is 
a custom username.

####Responses
The server will respond with a `1` for success and `0` for errors. All responses are prepended with the api version as well.

For example successful communication with the server that is running api version `1.0.0` will look like the following.
>1.0.0:1

[Twisted]:https://twistedmatrix.com/trac/