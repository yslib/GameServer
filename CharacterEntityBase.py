from entity import *


class MsgCharacterEntityBase(MsgEntityBase):
    def __init__(self,msgtype,eid,etype,visible,owner,transform = Transform()):
        super(MsgCharacterEntityBase,self).__init__(msgtype,eid,etype,visible,owner,transform)
        self.appendParam('health', 100, 'i')
        self.appendParam('attackTargetEntityID', -1, 'i')
        self.appendParam('boardTargetEntityID', -1 ,'i')
        self.appendParam('score', 0, 'i')
        self.appendParam('animh',0.0,'f')
        self.appendParam('animv',0.0,'f')

class MsgCSCharacterEntityBase(MsgCharacterEntityBase):
    def __init__ (self,eid = -1 , etype = 0 ,visible = True,owner = -1,transform = Transform()):
        super (MsgCSCharacterEntityBase, self).__init__(conf.MSG_CS_ENTITY_CHARACTER_STATE,eid, etype, visible,owner, transform)


class MsgSCCharacterEntityState(MsgCharacterEntityBase):
    def __init__ (self,eid =-1 , etype  = 0,visible = True,owner = -1,transform = Transform()):
        super (MsgSCCharacterEntityState, self).__init__(conf.MSG_SC_ENTITY_CHARACTER_STATE_UPDATE, eid, etype, visible,owner, transform)


class MsgSCCharacterEntityCreation(MsgCharacterEntityBase):
    def __init__(self,eid, etype,visible,owner, transform):
        super(MsgSCCharacterEntityCreation, self).__init__(conf.MSG_SC_ENTITY_CHARACTER_CREATION, eid, etype, visible, owner,transform)

class CharacterEntityBase(EntityBase):
    def __init__(self, etype, transform):
        super(CharacterEntityBase, self).__init__(etype, transform)
        self.healthValue = 100
        self.attackTargetEntityID = -1
        self.attackDamage = 0
        self.animv = 0.0
        self.animh = 0.0

    def damaged(self, damage,attacker):
        self.needToBeUpdate == True
        self.healthValue -= damage
        if self.healthValue <= 0:
            self.needToBeDestroy = True

    def createMsgOf(self, msgType):
        msg = None
        if msgType == conf.MSG_SC_ENTITY_CHARACTER_CREATION:
            msg = MsgSCCharacterEntityCreation(self.id,self.type,self.visible,self.owner, self.transform)
            msg.health = self.healthValue
            msg.score = self.score
            msg.animv = self.animv
            msg.animh = self.animh
        elif msgType == conf.MSG_SC_ENTITY_CHARACTER_STATE_UPDATE:
            msg = MsgSCCharacterEntityState(self.id, self.type,self.visible,self.owner, self.transform)
            msg.health = self.healthValue
            msg.score = self.score
            msg.animv = self.animv
            msg.animh = self.animh
        elif msgType == conf.MSG_SC_ENTITY_DESTROY:
            msg = MsgEntityDestroy()
            msg.id = self.id
        else:
            raise TypeError()

        return msg.marshal()