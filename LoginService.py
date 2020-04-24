from dispatcher import Service
import conf
import json
import datetime
from header import *
from misc import Transform


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
            print "Host: ", who, " login successfully"
            rdata = MsgSCConfirm(who, 0).marshal()
            self.server.host.sendClient(who,rdata)
            ent = self.server.createPlayerEntity(Transform(10, 10, 10, 0, 0, 0, 1, 1, 1))
            ent.owner = who
            self.server.hid2eid[who] = ent.id
            # print "create player ", ent.id, datetime.datetime.now()
            self.server.sendGameInitMsgForClient(who)

    def handleLogout(self, msg, who):

        pass