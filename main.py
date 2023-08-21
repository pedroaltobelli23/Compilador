import sys
import math

n = len(sys.argv)
raw_chain = sys.argv[1]
# raw_chain = "1+1"
is_number = True
chain = "" 

#cleaning string
for char in raw_chain:
    if char != ' ':
        chain += char

number_initial = 0
number_final = 0
i=0
numbers = []
operations = []
#putting numbers in string
while i < len(chain):
    val = chain[i]
    if val == "+" or val=="-" or val=="*" or val=="/":
        number_final = i
        numbers.append(chain[number_initial:number_final])
        number_initial = i+1
        operations.append(val)
    i+=1
if number_initial!=number_final:
    numbers.append(chain[number_initial:])
    
total = int(numbers[0])

for i in range(len(operations)):
    operation = operations[i]
    next_number = int(numbers[i + 1])

    if operation == "+":
        total += next_number
    elif operation == "-":
        total -= next_number
    elif operation == "*":
        total *= next_number
    elif operation == "/":
        total /= next_number
    else:
        print("This operation don't exist")
        break
    
print(total)