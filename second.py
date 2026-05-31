def add(n1,n2):
    return n1+n2
def sub(n1,n2):
    if n1>n2:
        return n1-n2
    else:
        
        return f"reversing the order To make it positive or 0 value{n2-n1}"
    
    
def multi(n1,n2):
    return n1*n2

def divi(n1,n2):
    return n1/n2

def calculate(calc, n1, n2):
    return calc(n1,n2)

result = calculate(sub, 3,4)
print(result)














# import app

# app.main() # this will throw file name is app.py