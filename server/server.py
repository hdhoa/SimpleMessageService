#!/usr/bin/env python

import asyncio
import websockets
import json
import config as cfg

wsfromid = dict()

async def consumer(websocket, message):
	data= json.loads(message)
	if 'login' in data : 
		wsfromid[data['login']] = websocket
	else :
		if ('from' in data) and ('to' in data) and ('msg' in data) :
		#	print( 'send '+ data['msg'] + ' from ' + data['from'] + ' to ' + data['to'])
			ws = wsfromid[data['to']]
			try :
				await ws.send(str(message))
			except websockets.exceptions.ConnectionClosed :
				id=data['to']
				print('connection to '  + id + ' closed')
				del wsfromid[id]



async def handler(websocket, path):
	while True:
		message = await websocket.recv()
		await consumer(websocket, message)	
			
        
#start_server = websockets.serve(handler, '127.0.0.1', 5678)
start_server = websockets.serve(handler, cfg.config['host'], cfg.config['port'])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
