class Enemy:

    '''
    Goal: Show Encapsulation
    - Display Zombie walking, speaking and attacking.
    - Display Zombie getting their health and attacking
    - Create constructor
    - Encapsulation for getting the type of enemy
    - Create a new Enemy Ogre who needs more attack than the Zombie
    '''

    # Encapsulation is used in object-oriented programming to hide the internal state of an object and only allow modification through methods.
    # This provides several benefits:
    # - Protects the integrity of the object by preventing outside code from modifying internal variables directly.
    # - Makes the code easier to maintain and update, since changes to internal implementation won't affect code that uses the class.
    # - Allows the creator of the class to enforce rules or logic when getting or setting values (e.g., through getter/setter methods).
    # - Improves security by making some attributes or methods private.
    #
    # In this Enemy class, the type of enemy is encapsulated (made private with '__'), and can only be accessed in a controlled way via get_type_of_enemy().

    def __init__(self, type_of_enemy, health_points = 10, attack_damage = 1):
        # private variables start with __ in python 
        self.__type_of_enemy = type_of_enemy 
        self.health_points = health_points
        self.attack_damage = attack_damage

    def talk(self):
        print(f"I am a {self.__type_of_enemy}. Be prepared to fight!")

    def walk_forward(self):
        print(f"{self.__type_of_enemy} moves closer to you")

    def attack(self):
        print(f"{self.__type_of_enemy} attacks for {self.attack_damage} damage")  

    def get_type_of_enemy(self):
        return self.__type_of_enemy