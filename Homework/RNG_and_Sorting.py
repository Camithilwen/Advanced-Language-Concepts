

#
# This function uses 'random' to create a list of numbers
# within a specified range.
#
def randomList(rangeLow, rangeHigh, listLength):
    import random
    r = random
    r.seed()
    randList = []
    while len(randList) < listLength:
        randList.append(r.randint(rangeLow, rangeHigh))
    return randList 

#
# This function mirrors the first function but uses
# the 'SystemRandom' class of 'secrets' instead of 'random'.
#
def secretsList(rangeLow, rangeHigh, listLength):
    import secrets
    s = secrets.SystemRandom()
    secList = []
    while len(secList) < listLength:
        secList.append(s.randrange(rangeLow, rangeHigh))
    return secList

#
# Call functions to generate lists of numbers between 1 and 16
#
randListA = randomList(1, 16, 100)
secListA = secretsList(1, 16, 100)

#
# Print results
#
print("List populated by random:", randListA, "\n")
print("List populated by System Random via secrets:", secListA, "\n")

#
# Imports the pandas module for additional statistics functions
#
import pandas

#
# Assign each random numbers list to a pandas Series and print a frequency table using .value_counts()
#
randSeriesA = pandas.Series(randListA)
secSeriesA = pandas.Series(secListA)
print("Frequency of random numbers:\n", randSeriesA.value_counts().to_string(), "\n")
print("Frequency of secrets numbers:\n", secSeriesA.value_counts().to_string(), "\n")
# The frequency distributions here appear pretty similar to me at first glance.
# But I would be curious to program this to run several times over and aggregate the results for a better sample.

#
# Repeat experiment with numbers 1-65535
#
randListB = randomList(1,65535,100)
secListB = secretsList(1, 65535, 100)
randSeriesB = pandas.Series(randListB)
secSeriesB = pandas.Series(secListB)
print("Frequency tables of numbers between 1-65535:\n")
print("Frequency of random numbers:\n", randSeriesB.value_counts().to_string(), "\n")
print("Frequency of secrets numbers:\n", secSeriesB.value_counts().to_string(), "\n")
#Both methods now output only unique values, wich makes sense considering the range of possible values.

#
# Merge sort algorithm developed from an example in my Data Structures textbook.
#
def basicMerge(inputList):
    copyBuffer = [None] * len(inputList)
    def sortStep(inputList, copyBuffer, low, high):
        if low < high:
            middle = (low + high) // 2
            sortStep(inputList, copyBuffer, low, middle)
            sortStep(inputList, copyBuffer, middle + 1, high)
            def merge(inputList, copyBuffer, low, middle, high):
                i1 = low
                i2 = middle + 1
                for i in range(low, high + 1):
                    if i1 > middle:
                        copyBuffer[i] = inputList[i2]
                        i2 += 1
                    elif i2 > high:
                        copyBuffer[i] = inputList[i1]
                        i1 += 1
                    elif inputList[i1] < inputList[i2]:
                        copyBuffer[i] = inputList[i1]
                        i1 += 1
                    else:
                        copyBuffer[i] = inputList[i2]
                        i2 += 1
                for i in range (low, high +1): 
                    inputList[i] = copyBuffer[i]
                return inputList
            returnList = merge(inputList, copyBuffer, low, middle, high)
            return returnList
    returnList = sortStep(inputList, copyBuffer, 0, len(inputList) - 1)
    return returnList

#
# Sort the lists of random numbers and record execution time for each. 
#

def sortTimer(sortMethod, inputList):
    import time
    if sortMethod == "merge":
        start = time.time()
        sortedList = basicMerge(inputList)
        end = time.time()
    elif sortMethod == "Powersort":
        start = time.time()
        sortedList = sorted(inputList)
        end = time.time()
    else:
        print("Please enter a valid sort type.")
    print("Sort completed in", f"{end - start:.9f}", "seconds.")
    print("Sorted list:", sortedList, "\n")

print("Merge sort of 100 element list between 1 and 16:")
sortTimer("merge", randListA)
print("Powersort of 100 element list between 1 and 16:")
sortTimer("Powersort", randListA)
print("Merge sort of 100 element list between 1 and 65535:")
sortTimer("merge", randListB)
print("Powersort of 100 element list between 1 and 65535:")
sortTimer("Powersort", randListB)
#Observation of results indicates that Powersort is faster than merge sort alone.
#Sort times remain relatively constant between larger and smaller values given the same set length.

#
# Generate a 500 element list and compare sort times.
#
randListC = randomList(1, 65535, 500)
print("Merge sort of 500 element list between 1 and 65535:")
sortTimer("merge", randListC)
print("Powersort of 500 element list between 1 and 65535:")
sortTimer("Powersort", randListC)
#These results indicate that Powersort is substantially faster than merge sort alone.
#Given a greater set length, Powersort's time remained varied little, while merge sort's time increased by one decimal place.
#These differences are still minimal relative to other algorithm forms. Both merge sort methods remain highly time efficient.