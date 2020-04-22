
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

class EntityBase(object):
    def __init__(self,type,transform = Transform()):
        self.id = -1
        self.needToBeUpdate = False
        self.needToBeDestroy = False
        self.type = type
        self.transform = transform
        self.visible = True
        self.owner = -1
    def tick(self):
        pass

    def transformUpdate(self, newTransform):
        self.transform = newTransform
        pass

class CharacterEntityBase(EntityBase):
    def __init__(self, etype, transform):
        super(CharacterEntityBase, self).__init__(etype, transform)
        self.healthValue = 100
        self.attackTargetEntityID = -1
        self.attackDamage = 0

    def damaged(self, damage,attacker):
        self.healthValue -= damage
        if self.healthValue <= 0:
            self.needToBeDestroy = True

    def createMsgPackage(self):
        state = MsgSCCharacterEntityState(self.id,self.type,self.transform);
        state.health = self.healthValue
        state.attackTarget = -1
        state.attackDamage = 0
        return state.marshal()

class PlayerEntity(CharacterEntityBase):
    def __init__(self, transform):
        super(PlayerEntity, self).__init__(EntityType.Player, transform)
        self.attackDamage = 30
        self.boardTargetEntityID = -1
        self.score = 0

    def createMsgPackage(self):
        state = MsgSCCharacterEntityState(self.id, self.type, self.transform);
        state.health = self.healthValue
        state.score = self.score
        return state.marshal()

class EnemyEntity(CharacterEntityBase):
    def __init__(self, transform):
        super(EnemyEntity, self).__init__(EntityType.Enemy, transform)
        self.attackDamage = 5
        self.scoreValue = 5

    def createMsgPackage(self):
        state = MsgSCCharacterEntityState(self.id, self.type, self.transform);
        state.health = self.healthValue
        return state.marshal()


class TankEntity(CharacterEntityBase):
    def __init__(self, transform):
        super(TankEntity, self).__init__(EntityType.Vehicle, transform)
        self.healthValue = 200
        self.attackDamage = 50

    def board(self, hid):
        self.owner = hid

    def createMsgPackage(self):
        state = MsgSCCharacterEntityState(self.id, self.type, self.transform);
        state.health = self.healthValue
        return state.marshal()


class ServiceMessage(object):
    def __init__(self, sid, cid, data):
        self.sid = sid
        self.cid = cid
        self.data = data

class GameWorldService(Service):
    SERVICE_ID = conf.SVC_ID_GAMEWORLD
    def __init__(self, server):
        super(GameWorldService, self).__init__(server, GameWorldService.SERVICE_ID)
        cmds = {
            conf.GAMEWORLD_SVC_CMD_ID_ENTITY_STATE: self.handleEntityState
        }
        self.registers(cmds)

    def handleEntityState(self, msg, who):
        eid = msg.data.id
        if eid not in self.server.entities.keys():
            print "entity do not exists, ", eid
            return
        etype = msg.data.type
        owner = msg.data.owner
        transform = Transform()
        transform.xp = msg.data.xp
        transform.yp = msg.data.yp
        transform.zp = msg.data.zp
        transform.xr = msg.data.xr
        transform.yr = msg.data.yr
        transform.zr = msg.data.zr
        transform.xs = msg.data.xs
        transform.ys = msg.data.ys
        transform.zs = msg.data.zs
        attackTargetEntityID = msg.data.attackTargetEntityID
        boardTargetEntityID = msg.data.boardTargetEntityID
        print "handle entity state, id: ", eid, " etype: ", etype

        ent = self.server.entities[eid]

        # for all type
        # update transform
        ent.transform = transform

        # update attack state if does
        if attackTargetEntityID != -1:
            if attackTargetEntityID not in self.server.entities.keys():
                print ent.id, "attack target do not exist, ", attackTargetEntityID
            else:
               attackTarget = self.server.entities[attackTargetEntityID]
               attackTarget.damage(ent.attackDamage)
        # update board state if does
        if boardTargetEntityID != -1:
            if boardTargetEntityID not in self.server.entities.keys():
                print "board target do not exist, ", boardTargetEntityID
            if ent.boardTargetEntityID == -1:
                boardTarget = self.server.entities[boardTargetEntityID]
                if boardTarget.type != EntityType.Vehicle:
                    raise TypeError("the board target in not a vehicle")
                boardTarget.board(who)
                ent.boardTargetEntityID = boardTargetEntityID
            else:
                print "the player has already boarded"
                pass

    def handleAttack(self, msg, who):
        pass

    def handleBoard(self, msg, who):
        pass


class UserLoginService(Service):
    SERVICE_ID = conf.SVC_ID_LOG

    def __init__(self, server):
        super(UserLoginService, self).__init__(server, UserLoginService.SERVICE_ID)
        self.fileName = "user.json"
        self.user = None
        with open(self.fileName, 'r') as f:
            jsonText = f.read()
            print jsonText
            self.user = json.loads(jsonText)

        cmds = {
            conf.LOG_SVC_CMD_ID_LOGIN:self.handleLogin,
            conf.LOG_SVC_CMD_ID_LOGOUT:self.handleLogout
        }
        self.registers(cmds)

    def handleLogin(self, msg, who):
        if str(msg.data.name) not in self.user:
            # send message to inform that the user do not exist
            print "Host: ",who," fail to login, the username do not exist"
            rdata = MsgSCConfirm(who, 1).marshal()
            self.server.host.sendClient(who, rdata)
        elif str(msg.data.name) in self.user and str(msg.data.pwd) != self.user[str(msg.data.name)]:
            # login success
            print "Host: ",who," fail to login, the password is not correct"
            rdata = MsgSCConfirm(who, 2).marshal()
            self.server.host.sendClient(who, rdata)
        elif str(msg.data.name) in self.user and str(msg.data.pwd) == self.user[str(msg.data.name)]:
            print "Host: ",who," login successfully"
            rdata = MsgSCConfirm(who, 0).marshal()
            self.server.host.sendClient(who,rdata)
            ent = self.server.createPlayerEntity(Transform(10,10,10,0,0,0,1,1,1))
            ent.owner = who
            self.server.hid2eid[who] = ent.id
            print "create player ",ent.id

    def handleLogout(self, msg, who):

        pass
