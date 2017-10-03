#!/usr/bin/env python

import asyncio
import websockets
import json
import config as cfg

wsfromid = dict()

peers= set()

async def consumer(websocket, message):
	data= json.loads(message)
	if 'login' in data : 
		id=data['login']
		wsfromid[id] = websocket
		peers.add(id)
	else :
		if ('from' in data) and ('to' in data) and ('msg' in data) :
			to_id =data['to']
			if to_id in peer :
				ws = wsfromid[to_id]
				try :
					await ws.send(str(message))
				except websockets.exceptions.ConnectionClosed :
					data={'error' : 'connection to {} closed''.format(to_id)}
					websocket.send(json.dumps(data))
					del wsfromid[to_id]
			else :
				data={'error' : 'peer {} does not exist'.format(to_id)}
				websocket.send(json.dumps(data))


async def handler(websocket, path):
	while True:
		message = await websocket.recv()
		await consumer(websocket, message)	
			
        
#start_server = websockets.serve(handler, '127.0.0.1', 5678)
start_server = websockets.serve(handler, cfg.config['host'], cfg.config['port'])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
