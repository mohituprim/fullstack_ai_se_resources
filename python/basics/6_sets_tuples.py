"""
Sets are similar to lists but are unordered and cannot contain duplications
Use curly brackets

Tuples are immutable and can contain duplicates
Use small parantheses
"""

my_set = {1, 2, 3, 4, 5, 1, 2}
print(my_set)
# print(len(my_set))


# for x in my_set:
#     print(x)


# my_set.discard(3)
# print(my_set)
# my_set.add(6)
# print(my_set)
# my_set.update([7, 8])
# print(my_set)


my_tuple = (1, 2, 3, 4, 5, 3)
print(my_tuple)
# my_tuple[1] = 100  - TypeError: 'tuple' object does not support item assignment
