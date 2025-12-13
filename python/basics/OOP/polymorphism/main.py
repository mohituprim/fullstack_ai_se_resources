from Zombie import *
from Ogre import *
from Enemy import *

def battle(e: Enemy):
    e.talk()
    e.attack()

zombie = Zombie(10, 1)
ogre = Ogre(20, 3)

battle(zombie)
battle(ogre)

#  Another Example
listEnemy: Enemy = []

e = Enemy('Enemy', 2, 1)
z = Zombie(10, 1)
o = Ogre(20, 3)

listEnemy.append(e)
listEnemy.append(z)
listEnemy.append(o)

for enemy in listEnemy:
    enemy.talk()