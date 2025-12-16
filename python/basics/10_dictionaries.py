"""
Dictionaries
"""


user_dictionary = {
    'username': 'codingwithmohit',
    'name': 'Eric',
    'age': 32
}

print(user_dictionary.get("age"))
user_dictionary2 = user_dictionary.copy()
user_dictionary2.pop("age")
print(user_dictionary2)

"""
Based on the dictionary:
my_vehicle = {
    "model": "Ford",
    "make": "Explorer",
    "year": 2018,
    "mileage": 40000
}
 - Create a for loop to print all keys and values
 - Create a new variable vehicle2, which is a copy of my_vehicle
 - Add a new key 'number_of_tires' to the vehicle2 variable that is equal to 4
 - Delete the mileage key and value from vehicle2
 - Print just the keys from vehicle2
"""


my_vehicle = {
    "model": "Ford",
    "make": "Explorer",
    "year": 2018,
    "mileage": 40000
}

#  printk key value 
for x, y in my_vehicle.items():
    print(x, y)


vehicle2 = my_vehicle.copy()


vehicle2["number_of_tires"] = 4


vehicle2.pop("mileage")


# print keys
for i in vehicle2:
    print(i)

"""
Notes:
- Dictionaries: unordered mappings of unique, hashable keys to values. Keys must be immutable (str, int, tuple of immutables, etc.); values can be anything. Lookups/sets are average O(1). Preserve insertion order (CPython 3.7+). Common ops: `.get()`, `.items()`, `.keys()`, `.values()`, `.pop()`, `.update()`, `in` for key membership, `.copy()` for shallow copies.
- Tuples: immutable, ordered sequences. Support indexing/slicing, packing/unpacking, iteration, can serve as dict keys if all elements are hashable. Good for fixed-size records (e.g., coordinates), returning multiple values, and protecting data from accidental modification. Use namedtuple/dataclass for readability if many fields are involved.
"""