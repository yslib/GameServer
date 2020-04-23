from CharacterEntityBase import CharacterEntityBase,MsgSCCharacterEntityState
from entity import  EntityType

class EnemyEntity(CharacterEntityBase):
    def __init__(self, transform):
        super(EnemyEntity, self).__init__(EntityType.Enemy, transform)
        self.attackDamage = 5
        self.scoreValue = 5


    def damaged(self, damage,attacker):
        super(EnemyEntity, self).damaged(damage,attacker)

