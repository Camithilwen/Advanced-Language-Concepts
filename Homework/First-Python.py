import array
import random
random1 = random
random1.seed(10)
test1 = random1.randint(1, 10)
test2 = random1.randint(3,20)
test3 = random1.randint(5, 40)
array1 = [test1, test2, test3]
for x in array1:
    print(x)
 