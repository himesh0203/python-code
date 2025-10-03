# Creating a string
name = "Alice"

# Accessing characters
print(name[0])  # Output: A

# String methods
print(name.lower())  # alice
print(name.upper())  # ALICE
print(len(name))     # 5







fruits = ["apple", "banana", "cherry"]

# Access
print(fruits[1])  # banana

# Modify
fruits[0] = "orange"

# Add
fruits.append("mango")

# Remove
fruits.remove("banana")

print(fruits)  # ['orange', 'cherry', 'mango']







coordinates = (10, 20)

print(coordinates[0])  # 10

# coordinates[0] = 15  # ❌ Error: Tuples can't be changed








person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Access
print(person["name"])  # John

# Modify
person["age"] = 31

# Add
person["job"] = "Engineer"

# Remove
del person["city"]

print(person)







numbers = {1, 2, 3, 2, 1}
print(numbers)  # {1, 2, 3} — duplicates removed

# Add
numbers.add(4)

# Remove
numbers.remove(2)







import array

arr = array.array('i', [1, 2, 3])  # 'i' = typecode for int

arr.append(4)
print(arr)  # array('i', [1, 2, 3, 4])





x = 10

if x > 0:
    print("Positive")
elif x == 0:
    print("Zero")
else:
    print("Negative")







# Loop through a list
for fruit in ["apple", "banana", "mango"]:
    print(fruit)

# Loop through range
for i in range(5):
    print(i)






count = 0
while count < 5:
    print(count)
    count += 1







# break
for i in range(5):
    if i == 3:
        break
    print(i)

# continue
for i in range(5):
    if i == 3:
        continue
    print(i)

# pass (used as a placeholder)
for i in range(5):
    pass  # Does nothing for now



