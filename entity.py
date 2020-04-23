
from dispatcher import Service
import conf
from events import *

from misc import Transform
import struct
import json

class EntityType(object):
    Vehicle = 0
    Player = 1
    Enemy = 2
    Shell = 3



class EntityBase(object):
    def __init__(self,type ,transform = Transform()):
        self.id = -1
        self.needToBeUpdate = False
        self.needToBeDestroy = False
        self.needToBeCreated = True
        self.type = type
        self.transform = transform
        self.visible = True
        self.owner = -1

    def createMsgOf(self,msgType):
        raise NotImplementedError("createMsgOf() is not implemented")

    def tick(self):
        # check state and pack the msg send to client
        raise NotImplementedError("tick() method is not implemented")
        pass

    def transformUpdate(self, newTransform):
        self.transform = newTransform
        pass


class MsgEntityBase(SimpleHeader):
    def __init__(self,msgtype,id,etype,visible = True,owner = -1,transform = Transform()):
        super(MsgEntityBase,self).__init__(msgtype)
        self.appendParam('id',id,'i')
        self.appendParam('type', etype, 'i')
        self.appendParam('visible', visible, '?')
        self.appendParam('owner', owner, 'i')
        self.appendParam('xp', transform.xp, 'f')
        self.appendParam('yp', transform.yp, 'f')
        self.appendParam('zp', transform.zp, 'f')
        self.appendParam('xr', transform.xr, 'f')
        self.appendParam('yr', transform.yr, 'f')
        self.appendParam('zr', transform.zr, 'f')
        self.appendParam('xs', transform.xs, 'f')
        self.appendParam('ys', transform.ys, 'f')
        self.appendParam('zs', transform.zs, 'f')

class MsgEntityDestroy(SimpleHeader):
    def __init__(self):
        super(MsgEntityDestroy, self).__init__(conf.MSG_SC_ENTITY_DESTROY)
        self.appendParam('id',-1,'i')


