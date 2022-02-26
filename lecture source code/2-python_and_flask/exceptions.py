a = int(input("a: "))
b = int(input("b: "))
try:
    print(f"{a} / {b} = {a / b}")
except ZeroDivisionError:
    print("Cannnot divide by 0")
