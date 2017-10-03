#!/usr/bin/env python

import asyncio
import websockets
import json
import config as cfg
import signal
import sys
import functools
import pickle
import os

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
	global msgqueue
	if id in msgqueue :
		msgqueue[id].append(message)
	else :
		msgqueue[id] = [message]
	

def retrieve_msg(id) :
	global msgqueue
	if id in msgqueue :
		msgs=  msgqueue[id]
		msgqueue[id] =[]
		return msgs
	else :
		return None

async def handler(websocket, path):
	while True:
		message = await websocket.recv()
		await consumer(websocket, message)	
			
def shutdown(loop) :
	print('Exit, saving data')
	try:
		saveData(cfg.config['data_dir'])
	finally:
		sys.exit(0)

def loadData(datadir) :
	try:
		global peers
		peersF = open(datadir+'/peers','rb') 	
		peers = pickle.load(peersF)
		peersF.close()
		print ('already known peers '+ str(peers))
	except Exception :
		print('no previous peers to retrieve')
	try:	
		global msgqueue
		msgsF = open(datadir+'/msgqueue','rb') 
		msgqueue= pickle.load(msgsF)
		msgsF.close()
		print ('msq waiting queue '+ str(msgqueue))
	except Exception :
		print('no previous messages to retrieve')	

def saveData(datadir) : 
	peersF = open(datadir+'/peers','wb') 
	pickle.dump(peers, peersF )
	peersF.close()
	msgsF = open(datadir+'/msgqueue','wb') 
	pickle.dump(msgqueue, msgsF)
	msgsF.close()


def main():
	if not os.path.exists(cfg.config['data_dir']):
		os.makedirs(cfg.config['data_dir'])
			
	loadData(cfg.config['data_dir'])
	start_server = websockets.serve(handler, cfg.config['host'], cfg.config['port'])
	loop=asyncio.get_event_loop()
	
	for signame in ('SIGINT','SIGTERM', 'SIGHUP'):
		loop.add_signal_handler(getattr(signal, signame), functools.partial(shutdown, loop))
		
	loop.run_until_complete(start_server)
	loop.run_forever()

if __name__ == '__main__':
    main()