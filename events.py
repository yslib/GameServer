# -*- coding: GBK -*-
import conf
from header import SimpleHeader
from misc import Transform


class MsgEntityBase(SimpleHeader):
	def __init__(self,id,etype,msgtype,transform = Transform()):
		super(MsgEntityBase,self).__init__(msgtype)
		self.appendParam('id',id,'i')
		self.appendParam('type', etype, 'i')
		self.appendParam('visible', True, '?')
		self.appendParam('owner', -1, 'i')
		self.appendParam('xp', transform.xp, 'f')
		self.appendParam('yp', transform.yp, 'f')
		self.appendParam('zp', transform.zp, 'f')
		self.appendParam('xr', transform.xr, 'f')
		self.appendParam('yr', transform.yr, 'f')
		self.appendParam('zr', transform.zr, 'f')
		self.appendParam('xs', transform.xs, 'f')
		self.appendParam('ys', transform.ys, 'f')
		self.appendParam('zs', transform.zs, 'f')


class MsgCSLogin(SimpleHeader):
	def __init__(self, name = -1, pwd = -1):
		super(MsgCSLogin, self).__init__(conf.MSG_CS_LOGIN)
		self.appendParam('name', name, 's')
		self.appendParam('pwd', pwd, 's')

class MsgCSLogout(SimpleHeader):
	def __init__(self,hid = -1):
		super(MsgCSLogout,self).__init__(conf.MSG_CS_LOGOUT)

class MsgSCConfirm(SimpleHeader):
	def __init__(self, uid = 0, result = 0):
		super (MsgSCConfirm, self).__init__(conf.MSG_SC_CONFIRM)
		self.appendParam('uid', uid, 'i')
		self.appendParam('result', result, 'i')


class MsgCharacterEntityBase(MsgEntityBase):
	def __init__(self,eid,etype,msgType,transform = Transform()):
		super(MsgCharacterEntityBase,self).__init__(eid,etype,msgType,transform)
		self.appendParam('health', 100, 'i')
		self.appendParam('attackTargetEntityID', -1, 'i')
		self.appendParam('score', 0, 'i')

class MsgCSCharacterEntityBase(MsgCharacterEntityBase):
	def __init__ (self,eid, etype,transform = Transform()):
		super (MsgCSCharacterEntityBase, self).__init__(eid, etype, conf.MSG_CS_CHARACTER_STATE, transform)

class MsgSCCharacterEntityState(MsgCharacterEntityBase):
	def __init__ (self,eid, etype,transform):
		super (MsgSCCharacterEntityState, self).__init__(eid, etype, conf.MSG_SC_CHARACTER_STATE, transform)



class MsgSCEntityCreation(MsgEntityBase):
	def __init__(self, etype, transform):
		super(MsgSCEntityCreation,self).__init__(etype,conf.MSG_SC_ENTITY_CREATION,transform)

