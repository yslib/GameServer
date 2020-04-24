import sys
from events import *
from entity import *
from dispatcher import Dispatcher,ServiceMessage
from simpleHost import SimpleHost
from timer import TimerManager
import struct
import time
from GameWorldService import GameWorldService
from CharacterEntityBase import MsgSCCharacterEntityState, MsgCSCharacterEntityBase
from LoginService import UserLoginService, MsgSCConfirm, MsgCSLogin
from PlayerEntity import PlayerEntity
from EnemyEntity import  EnemyEntity
from TankEntity import TankEntity


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
		print "generated eid: ", eid
		self.entities[eid] = entity
		return

	# update for every ticks
	def sendEntityUpdateMsgForAllClient(self):
		for eid, e in self.entities.items():
			if e is not None:
				if e.state == EntityState.NeedToBeUpdated:
					self.host.sendClientExcept(e.owner, e.createMsgOf(conf.MSG_SC_ENTITY_CHARACTER_STATE_UPDATE))
					e.state = EntityState.NeedToDoNothing
					print "state: ",e.state," update entity ", e.id, " except for ", e.owner
				elif e.state == EntityState.NeedToBeCreated:
					self.host.broadcast(e.createMsgOf(conf.MSG_SC_ENTITY_CHARACTER_STATE_UPDATE))
					e.state = EntityState.NeedToDoNothing
					print self.entities[1].state
					print "state: ",e.state," create entity ", e.id, " for all clients",
				elif e.state == EntityState.NeedToBeDestroyed:
					self.host.broadcast(e.createMsgOf(conf.MSG_SC_ENTITY_DESTROY))
					# TODO::
					e.state = EntityState.NeedToDoNothing
					print "destroy entity ", e.id, " for all clients",
				elif e.state != EntityState.NeedToDoNothing:
					raise TypeError("entity state error")

	# calling for a new client
	def sendGameInitMsgForClient(self, hid):
		for eid, e in self.entities.items():
			if e is not None and e.state == EntityState.NeedToDoNothing:
				self.host.sendClient(hid, e.createMsgOf(conf.MSG_SC_ENTITY_CHARACTER_STATE_UPDATE))
				print "create entity ", e.id, " for ", hid
	#
	# def sendEntityCreateionMsgForClient(self, hid, eid):
	# 	if eid in self.entities.keys():
	# 		self.host.sendClient(hid, self.entities[eid].createMsgOf(conf.MSG_SC_ENTITY_CHARACTER_CREATION))
	#
	# def sendEntityDistroyMsgForAllClient(self,hid,eid):
	# 	pass


	def createPlayerEntity(self, transform):
		ent = PlayerEntity(transform)
		ent.state = EntityState.NeedToBeCreated
		self.registerEntity(ent)
		self.gameWorldService.addEntityListener(ent.id)

		return ent

	def createTankEntity(self, transform):
		ent = TankEntity(transform)
		ent.state = EntityState.NeedToBeCreated
		self.registerEntity(ent)
		self.gameWorldService.addEntityListener(ent.id)
		return ent

	def createEnemyEntity(self, transform):
		ent = EnemyEntity(transform)
		ent.state = EntityState.NeedToBeCreated
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
			if sid == conf.SVC_ID_GAMEWORLD:
				if cid == conf.GAMEWORLD_SVC_CMD_ID_ENTITY_STATE:
					data = MsgCSCharacterEntityBase().unmarshal(content)
					self.dispatcher.dispatch(ServiceMessage(sid, cid, data), param)
			elif sid == conf.SVC_ID_LOG:
				data = MsgCSLogin().unmarshal(content)
				self.dispatcher.dispatch(ServiceMessage(sid, cid, data), param)
			else:
				raise TypeError("Unknown service id")

		elif event == conf.NET_CONNECTION_NEW:
			# self.createGameWorldForNewClient(param)
			pass
		elif event == conf.NET_CONNECTION_LEAVE:
			pass

		self.sendEntityUpdateMsgForAllClient()
		# for eid, entity in self.entities.iteritems():
		# 	# Note: you can not delete entity in tick.
		# 	# you may cache delete items and delete in next frame
		# 	# or just use items.
		# 	entity.tick()
		return


if __name__ =="__main__":

	port = 2000
	server = SimpleServer()
	server.host.startup(port)
	print "Listen at "+str(port)

	while 1:
		server.tick()
		# test timer
		TimerManager.addRepeatTimer(0.015, server.addCount)
		last = time.time()
		while 1:
			time.sleep(0.01)
			TimerManager.scheduler()
			if time.time() - last > 0.01:
				break
