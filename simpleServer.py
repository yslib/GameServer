
import sys
from events import *
from entity import *
from dispatcher import Dispatcher
from simpleHost import SimpleHost
from timer import TimerManager
import struct
import time
class SimpleServer(object):
	
	def __init__(self):

		super(SimpleServer, self).__init__()

		self.hid2eid = {}

		self.entities = {}
		self.entityIndex = 1

		self.host = SimpleHost()
		self.dispatcher = Dispatcher()

		self.gameWorldService = GameWorldService(self)
		self.userLoginService = UserLoginService(self)

		self.dispatcher.register(GameWorldService.SERVICE_ID, self.gameWorldService)
		self.dispatcher.register(UserLoginService.SERVICE_ID, self.userLoginService)

		self.count = 0
		return

	def generateEntityID(self):
		id = self.entityIndex
		self.entityIndex += 1
		return id

	def registerEntity(self, entity):
		eid = self.generateEntityID()
		entity.id = eid
		self.entities[eid] = entity
		return

	# update for every ticks
	def updateGameWorldForClients(self):
		for eid,e in self.entities.items():
			if e is not None and e.needToBeUpdate == True:
				self.host.broadcast(e.createMsgPackage())
				e.needToBeUpdate = False

	# calling for a new client
	def updateGameWorldForClient(self, hid):
		for eid, e in self.entities.items():
			if e is not None:
				self.host.sendClientExcept(hid,e.createMsgPackage())

	def createPlayerEntity(self, transform):
		ent = PlayerEntity(transform)
		ent.needToBeUpdate = True
		self.registerEntity(ent)
		self.gameWorldService.addEntityListener(ent.id)
		return ent

	def createTankEntity(self,transform):
		ent = TankEntity(transform)
		ent.needToBeUpdate = True
		self.registerEntity(ent)
		self.gameWorldService.addEntityListener(ent.id)
		return ent

	def createEnemyEntity(self,transform):
		ent = EnemyEntity(transform)
		ent.needToBeUpdate = True
		self.registerEntity(ent)
		self.gameWorldService.addEntityListener(ent.id)
		return ent

	def addCount(self):
		self.count += 1

	def tick(self):
		self.host.process()
		event, param, rdata = self.host.read()
		if event == conf.NET_CONNECTION_DATA:
			sid, cid = struct.unpack("<HH", rdata[0:4])
			content = rdata[4:]
			print "sid: ", sid, " cid: ", cid
			if sid == conf.SVC_ID_GAMEWORLD:
				if cid == conf.GAMEWORLD_SVC_CMD_ID_ENTITY_STATE:
					data = MsgCSCharacterEntityBase().unmarshal(content)
					self.dispatcher.dispatch(ServiceMessage(sid, cid, data), param)
			elif sid == conf.SVC_ID_LOG:
				data = MsgCSLogin().unmarshal(content)
				self.dispatcher.dispatch(ServiceMessage(sid, cid, data), param)
			else:
				raise TypeError("Unknown SVI_ID")

		self.updateGameWorldForClients()


		# for eid, entity in self.entities.iteritems():
		# 	# Note: you can not delete entity in tick.
		# 	# you may cache delete items and delete in next frame
		# 	# or just use items.
		# 	entity.tick()
		return

def encode(s):
	return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

if __name__ =="__main__":

	port = 2000
	server = SimpleServer()
	server.host.startup(port)
	print "Listen at "+str(port)

	while 1:
		server.tick()
		# test timer
		TimerManager.addRepeatTimer(0.15, server.addCount)
		last = time.time()
		while 1:
			time.sleep(0.01)
			TimerManager.scheduler()

			if time.time() - last > 1.0:
				break
