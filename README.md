# SimpleMessageService


## How to test with our simple client

_Note that I have several version on python running on my laptop, to handle old projects._
_For this project I have used python 3.6.2._

In order to run this project, you will have to :
* install the websockets python library :

```
pip3 install websockets
```

* clone the project

* from the cli, run :
```
sh start_client.sh
python3 server/server.py
```

You may have to change python3 to python depending on your setup 

* open two browser windows on http://localhost:8000
* log as user A and user B
* you can send message between users
* when a peer disconnects from the server, messages will be stored and delivered when it comes bak
* if you shutdown and restart the server, the list of known peers and the message queue will be restored

## How to test with your own client

* The server listens on ws://127.0.0.1:5678/

The host and port can be configured in server/config.py

* On connection, in order to log in, the server expects a json object of the following type :

```
{'login':'name of the peer'}
```
Note that the login automatically registers the peer to the server (there is no create user phase, as we do not handle security anyway).

* To send a message, the server expects json objects of the following type :

```
{'from':'name of the sender', 'to':'name of the destination', 'msg':'message as a string' }
```
If the destination peer B does not exist, you will receive a json object : 

```
{'error': 'peer B does not exist'}
```

If the destination peer B is disconnected, you will receive a json object : 

```
{'error': 'connection to B closed'}
```

## Questions

### Which share of web users will this implementation address? Should it be increased and how?

This app is build on top of  the python [Websocket](https://websockets.readthedocs.io/en/stable/) library, which  implements  [RFC6455](https://tools.ietf.org/html/rfc6455)

As we can see on the [websockets wiki page](https://en.wikipedia.org/wiki/WebSocket#Browser_implementation) , this protocol is supported by all major browsers.

Therefore I think using this techno is ok, as it adresses most users.

### How many users can connect to one server?

A [websocket is a TCP Socket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers).
I would therefore think that since we maintain one websocket per user, we would be limited by the number of available file descriptors.

However after some research is seems that [much more] {https://en.wikipedia.org/wiki/C10k_problem} is possible.

### How can the system support more systems?

I'm not sure about this question.
Is it about supporting more users?

#### We could simply run several instances of this standalone server.
Users on different servers would not be able to communicate but in this case that may not be an issue : since we want to establish 
peer to peer connections to share video, I surmise that one of the criterium of choice is proximity.

Therefore, we could have a load balancer that distributes the clients based on a geographic base. 
Peers would be limited on the choice of other peers to stream from without affecting performances too much.

#### If any peer should be able to communicate with any other peers

This is more complicated, as we do not want the servers to  have to route message between each other.

We could :
* Instantiate several servers, who share a global list of peers (for example in a shared REDIS)
* Use a standard hash function to decide on which server a peer A should open a socket to receive messages 
* In order to write to peer B, peer A uses the same hash function to know to which server S the peer B is listening to
* A sends a message to S but do not maintain a connection

### How to reduce the attack surface of the systems?
### Should an authentication mechanism be put in place and if yes, how?

Yes, as we may want to distribute a video only for paying users, for example.

