from Enemy import *

zombie = Enemy()

#  assign type_of_enemy as it is not initialized with default under Enemy class
zombie.type_of_enemy = 'Zombie' 
print(f'{zombie.type_of_enemy} has {zombie.health_points} health points and can do attack of {zombie.attack_damage}')

zombie.talk()
zombie.walk_forward()
zombie.attack()