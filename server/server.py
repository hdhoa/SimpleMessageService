#!/usr/bin/env python

import asyncio
import websockets
import json
import config as cfg

wsfromid = dict()

peers= set()
connected_peers = set()

msgqueue=dict()

async def consumer(websocket, message):
	data= json.loads(message)
	if 'login' in data : 
		id=data['login']
		await login(id, websocket)
	else :
		if ('from' in data) and ('to' in data) and ('msg' in data) :
			to_id =data['to']
			if to_id in peers :
				if to_id in connected_peers :
					ws = wsfromid[to_id]
					try :
						await ws.send(str(message))
					except websockets.exceptions.ConnectionClosed :
						await peer_offline(websocket, to_id, message)
						del wsfromid[to_id]
						connected_peers.remove(to_id)
				else :
					await peer_offline(websocket, to_id, message)
			else :
				data={'error' : 'peer {} does not exist'.format(to_id)}
				await websocket.send(json.dumps(data))

async def login( id, websocket) :
	wsfromid[id] = websocket
	peers.add(id)
	connected_peers.add(id)
	waiting_msg =retrieve_msg(id)
	if not( waiting_msg is None) :
		for msg in waiting_msg :
			await websocket.send(msg)

async def peer_offline(websockersrc, iddest, message) :
	data={'error' : 'connection to {} closed, messages will be send as {} comes back online'.format(iddest, iddest)}
	await websockersrc.send(json.dumps(data))
	store_msg(iddest, str(message))


def store_msg(id, message):
	if id in msgqueue :
		msgqueue[id].append(message)
	else :
		msgqueue[id] = [message]
	

def retrieve_msg(id) :
	if id in msgqueue :
		msgs=  msgqueue[id]
		msgqueue[id] =[]
		return msgs
	else :
		return None

async def handler(websocket, path):
	while True:
		try :
			message = await websocket.recv()
			await consumer(websocket, message)	
			
        
#start_server = websockets.serve(handler, '127.0.0.1', 5678)
start_server = websockets.serve(handler, cfg.config['host'], cfg.config['port'])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
