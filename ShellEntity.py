
from entity import EntityType
from entity import EntityBase
from misc import Transform

class ShellEntity(EntityBase):
    def __init__(self,transform = Transform()):
        super(ShellEntity,self).__init__(EntityType.Shell, transform)
        self.attackDamage = 50

