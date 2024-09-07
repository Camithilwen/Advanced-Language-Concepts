"""
Jamie Kemman
9/7/2024
"""
#
#  Declare structures
#
toBeRead_Set = {"Lord of the Flies", "These Fevered Days", "The Odyssey", "All the Light We Cannot See", "Six of Crows", "Howl's Moving Castle", "The Last Days of Jeanne d'Arc", "The Bell Jar", "Where to Park Your Broomstick", "Eartheater"}
toBeRead_Dictionary = {"Dolores Reyes": "Eartheater", "Lauren Manoy": "Where to Park Your Broomstick", "Sylvia Plath": "The Bell Jar", "Ali Alizadeh": "The Last Days of Jeanne d'Arc", "Diana Wynne Jones": "Howl's Moving Castle", "Leigh Bardugo": "Six of Crows", "Anthony Doerr": "All the Light We Cannot See", "Emily Wilson": "The Odyssey", "Martha Ackmann": "These Fevered Days", "William Golding": "Lord of the Flies"}

#
#  Print third element of structures
#
for x in toBeRead_Set:
    if "Odyssey" in x:
        print("Set:", x)
        break
print("Dictionary:", toBeRead_Dictionary["Sylvia Plath"])
print()

#
#  Print structures in random order
#
print("Set in random order:", toBeRead_Set)
def printDict_Random(dictionary):
    printSet = {None}
    for x in dictionary:
        printSet.add(dictionary[x])
    print("Dictionary in random order:", printSet)
print()
printDict_Random(toBeRead_Dictionary)
print()

#
#  Add 11th element to structures
#
toBeRead_Set.add("Stamped from the Beginning")
toBeRead_Dictionary.update({"Ibram X. Kendi": "Stamped from the Beginning"})
print("11th set element added:", toBeRead_Set)
print()
print("11th dictionary element added:", toBeRead_Dictionary)
print()

#
#  Remove first element from structures
#
for x in toBeRead_Set:
    if "Lord" in x:
        toBeRead_Set.remove("Lord of the Flies")
        break
del toBeRead_Dictionary["Dolores Reyes"]
print("First set element removed:", toBeRead_Set)
print()
print("First dictionary element removed:", toBeRead_Dictionary)
print()

#
#  Remove the same element from structures
#
for x in toBeRead_Set:
    if "Fevered" in x:
        toBeRead_Set.remove(x)
        break
del toBeRead_Dictionary["Martha Ackmann"]
print("Same set element removed:", toBeRead_Set)
print()
print("Same dictionary element removed:", toBeRead_Dictionary)
print()