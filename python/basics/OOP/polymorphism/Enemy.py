class Enemy:

    '''
        Show Polymorphism
    '''

    # Polymorphism is the ability of different objects to respond, each in their own way, to the same method or function call.
    # The main benefit of polymorphism is that it allows for flexible and reusable code: 
    # you can write functions and methods that work on the superclass, but automatically call the overridden methods 
    # in the subclass based on the object's actual type at runtime.
    # 
    # In this example, the Enemy class defines a 'talk' method, and its subclasses (like Zombie and Ogre) override this method.
    # In main.py, the 'battle' function takes an Enemy object and calls e.talk() and e.attack().
    # Even though 'battle' expects an Enemy, if you pass a Zombie or Ogre, Python will call the overridden 'talk' method, 
    # demonstrating polymorphism in action.

    def __init__(self, type_of_enemy, health_points, attack_damage):
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