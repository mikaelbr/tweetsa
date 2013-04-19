
Installing and Starting
=====================


To start the sentiment analysis servers, there are two steps:

1. Start the Sentiment Classification Server
2. Start the API Layer

As an optional third step:

3. Start the visualization applications. 



## Start the Sentiment Classification Server:

Starting from the root of the code base:

```
➜  code git:(master) ✗ l
README.md
apilayer
apps
dataset
sentiment_server
```

1. Change directory to sentiment_server: ```$ cd sentiment_server/```
2. Start the sentiment server: ```$ python main.py```

This will start the server on ```http://localhost:7000/``` and it will listen for requests. 
This server should be started in ```screen``` if possible.

To see help run the following: ```python main.py -h```.


## Start the API Layer Server:

Again, starting from the root of the code base:

```
➜  code git:(master) ✗ l
README.md
apilayer
apps
dataset
sentiment_server
```

1. Change directory to apilayer: ```$ cd apilayer/```
2. Start the API Layer: ```$ npm start```

This will start the server on ```http://localhost:8088/``` and it will per default send requests
to ```http://localhost:7000/```. This server should be started in ```screen``` with ```forever``` if possible.

If you want to change the connection point to the sentiment server, this can be done by changing the ```config/default.js``` file. 
To change the port, env varibales can be used:

```
$ export PORT=7007
$ npm start
Express server listening on port 7007 in development mode
```

## Installing and starting SentiMap

Assuming you cloned the repository from Github you need to install the dependencies of the project. 
There are two types of deps: server-side and client-side. 

### Installing server-side dependencies

From the ```sentimap``` root folder, use NPM to install modules: ```npm install```.

### Installing client-side dependencies

Use Bower package manager to install dependencies: ```bower install```. 
(Assuming you are in sentimap root dir).

To install bower you can do: ```sudo npm install -g bower```.


## Installing and starting SentiSearch

To come.

