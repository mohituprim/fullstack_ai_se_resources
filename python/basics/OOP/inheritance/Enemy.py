class Enemy:

    '''
    Goal: Show Inheritance
    - Implement Zombie object
    - Explain Superclass / super()
    - Override talk function
    - Create SpreadDisease that Parent does not have
    - Create Ogre class
    - Implement Smash
    '''
    # Inheritance is a fundamental concept in object-oriented programming (OOP) that allows a class (called a subclass or derived class)
    # to inherit attributes and methods from another class (called a superclass or base class). This promotes code reuse and establishes a
    # hierarchical relationship between classes.
    #
    # Benefits of inheritance:
    # - Code Reusability: Common functionality can be defined in the superclass and reused in multiple subclasses, reducing code duplication.
    # - Extensibility: Subclasses can extend or override the behavior of the superclass, allowing for flexible enhancements.
    # - Maintainability: Changes in the superclass automatically propagate to subclasses, making code easier to maintain.
    # - Logical Structure: Helps organize code into a clear, hierarchical structure reflecting real-world relationships.

    # Method override is when a subclass provides its own implementation of a method that is already defined in its superclass. 
    # This allows the subclass to alter or extend the behavior of that method specifically for the subclass, while keeping the same method name and parameters.

    #
    # In Python, `self` is a reference to the current instance of the class.
    # It's used to access attributes and methods of the object from within its own class.
    #
    # `super()` is used to call methods of a superclass from a subclass. This is especially useful when you want to extend
    # or modify the behavior of inherited methods, or when you need to initialize the parent class from the child class.
    #
    # Example:
    #
    # class Animal:
    #     def __init__(self, name):
    #         self.name = name
    #
    # class Dog(Animal):
    #     def __init__(self, name, breed):
    #         super().__init__(name)  # Calls Animal's __init__, sets self.name
    #         self.breed = breed
    #     def speak(self):
    #         print(f"{self.name} barks!")
    #
    # Here, `self.name` accesses the name attribute of the object, while `super().__init__(name)` ensures that the initialization
    # from the base class is executed, setting up everything the parent expects.
    #
    # In this example codebase, Zombie and Ogre inherit from Enemy, use `super().__init__()` to properly initialize their base parts,
    # and access their own instance properties and methods using `self`.

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