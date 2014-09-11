Translation Studio Server
---

This repository contains the server side code for interacting with the Translation Studio app.

###Environment
The server script uses the [Twisted] library to create a web service that handles requests from the mobile app.

###Testing
To test on your local environment you'll need a tool that can communicate with a tcp port such as telnet.
Telnet is available on OSX by default, but you'll need to 
[manually enable telnet](http://technet.microsoft.com/en-us/library/cc771275(v=ws.10).aspx) it if using Windows 7.
Also, if you are using a windows environment make sure you install *all* of the dependencies. The laziest way to do that
is to try running the script and then installing whatever it tells you it's missing.

connect to the port (you may need to change the port)

>telnet 127.0.0.1 1234

send a message

>hello world

###Usage
The script expects to receive json data `{'key':'public key', 'udid':'device id', 'username':'an optional username'}`  
where `key` is the public ssh key of the mobile device, `udid` is the unique device id and the optional`usename` is 
a custom username.

###Responses
The server will send a json response back to the client which will include the api version and the response type and message.

For example successful communication with the server that is running api version `1.0.0` will look like the following.

>{"version":"1.0.0", "ok":"done"}

Or for an error message

>{"version":"1.0.0", "error":"incomplete request"}

###Configuration
The server loads a configuration file `config.json` upon startup. A full list of configuration options are described below

* **port** - the port on which the server will listen
* **key_path**:**user** - the path to which keys will be stored when the client provides a user name
* **key_path**:**device** - the path to which keys will be stored when the client only provides a udid.

For a complete configuration example see the `sample.config.json` file.


##Wish List
Below is a list of features that would be nice to have implemented in the future.

* Log requests to a file on the server

[Twisted]:https://twistedmatrix.com/trac/