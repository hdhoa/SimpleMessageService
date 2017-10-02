# SimpleMessageService


##How to test

Note that I have several version on python running on my laptop, to handle old projects.

For this project I have used python 3.6.2.

* install the websockets python library
pip3 install websockets

* clone the project

* from the cli, run :
sh start_client.sh
python3 server/server.py

You may have to change python3 to python depending on your setup 

* open two browser windows on http://localhost:8000
* log as user A and user B
* you can send message between users



## Questions

### Which share of web users will this implementation address? Should it be increased and how?

This app is build on top of  [Websocket](https://websockets.readthedocs.io/en/stable/).
websockets implements  [RFC6455](https://tools.ietf.org/html/rfc6455)
As we can see on the [websockets wiki page](https://en.wikipedia.org/wiki/WebSocket#Browser_implementation) , this protocol is implemented in all major browser

Therefore I think using websockets should be ok.


### How many users can connect to one server?

A [websocket is a TCP Socket] {https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers}.
I would therefore think that since we maintain one websocket per user, we would be limited by the number of available file descriptors.

However after some research is seems that [much more] {https://en.wikipedia.org/wiki/C10k_problem} is possible 

### How can the system support more systems?

I'm not sure about this question.
Is it about supporting more users?

* We could simply run several instances of this standalone server.
Users on different servers would not be able to communicate but in this case that may not be an issue.
We want to establish peer to peer connection to share video, and I surmise that one of the criterium of choice is proximity.
Therefore we could have a load balancer that distributes the clients based on a geographic base.
Peers would be limited on the choice of video sources without affecting performances.

* If any peer should be able to communicate with any other peers
 * we instantiate several  servers, who share a global list of peers (for example in a shared REDIS)
 * we use a standard hash function to decide on which server a peer A should open a socket to receive messages 
 * to write to peer B, peer A uses the same hash function to know to which server B is listening to
This supposes that peer A already knows peer B id. 


### How to reduce the attack surface of the systems?
### Should an authentication mechanism be put in place and if yes, how?

Yes, as we may want to distribute a video only for paying users, for example.
