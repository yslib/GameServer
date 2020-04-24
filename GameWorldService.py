from dispatcher import Service
import conf
from misc import Transform
from entity import EntityType,EntityState
import datetime


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
        #if eid not in self.server.entities.keys():
        #    print "entity do not exists, ", eid
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
        print "entityid: ", eid, " etype: ", etype, " host: ",who, "at ",datetime.datetime.now()
        ent = self.server.entities[eid]
        # for all type
        # update transform
        ent.transform = transform
        ent.state = EntityState.NeedToBeUpdated


        ent.animv = msg.data.animv
        ent.animh = msg.data.animh

        # print "anim:",ent.animv," ",ent.animv
        print "rot:",transform.xr,transform.yr,transform.zr

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
