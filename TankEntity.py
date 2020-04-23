from CharacterEntityBase import CharacterEntityBase,MsgSCCharacterEntityState

from entity import EntityType
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