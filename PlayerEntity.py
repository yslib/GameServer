from CharacterEntityBase import CharacterEntityBase,MsgSCCharacterEntityState,MsgSCCharacterEntityCreation
from events import *
from entity import  EntityType, MsgEntityDestroy


class PlayerEntity(CharacterEntityBase):
    def __init__(self, transform):
        super(PlayerEntity, self).__init__(EntityType.Player, transform)
        self.attackDamage = 30
        self.boardTargetEntityID = -1
        self.score = 0


