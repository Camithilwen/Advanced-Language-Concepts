

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

#
# Repeat experiment with numbers 1-65535
#
randSeriesB = pandas.Series(randomList(1, 65535, 100))
secSeriesB = pandas.Series(secretsList(1, 65535, 100))
print("Frequency tables of numbers between 1-65535:\n")
print("Frequency of random numbers:\n", randSeriesB.value_counts().to_string(), "\n")
print("Frequency of secrets numbers:\n", secSeriesB.value_counts().to_string(), "\n")
#Both methods now output only unique values, wich makes sense considering the range of possible values.

