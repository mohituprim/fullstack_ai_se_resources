class Enemy:

    type_of_enemy: str
    health_points: int = 10
    attack_damage: int = 1

    # Abstraction in object-oriented programming is used to hide complex implementation details 
    # and expose only the necessary, relevant parts of an object. This helps to reduce complexity 
    # and increase efficiency by allowing users to interact with objects at a higher level, 
    # without needing to understand the underlying code.
    #
    # In the Enemy class, abstraction can be implemented using an abstract base class if you want 
    # to enforce certain behaviors (like talk, walk_forward, attack) in all subclasses of Enemy. 
    # However, in this case, we're just providing the interface directly in the class.

    # Let's add a constructor to initialize our Enemy object:
    def __init__(self, type_of_enemy: str, health_points: int = 10, attack_damage: int = 1):
        self.type_of_enemy = type_of_enemy
        self.health_points = health_points
        self.attack_damage = attack_damage
    def talk(self):
        print(f"I am a {self.type_of_enemy}. Be prepared to fight!")

    def walk_forward(self):
        print(f"{self.type_of_enemy} moves closer to you")

    def attack(self):
        print(f"{self.type_of_enemy} attacks for {self.attack_damage} damage")  

    # To create an abstract class in Python, you use the 'abc' module and inherit from ABC.
    # You can define abstract methods using the @abstractmethod decorator.
    #
    # Example:
    #
    # from abc import ABC, abstractmethod
    #
    # class Enemy(ABC):
    #     @abstractmethod
    #     def talk(self):
    #         pass
    #     @abstractmethod
    #     def walk_forward(self):
    #         pass
    #     @abstractmethod
    #     def attack(self):
    #         pass
    #
    # Any subclass of Enemy would need to implement these methods.