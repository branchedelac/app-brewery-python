sum = float(input("The sum? "))
split = float(input("The people?? "))
tip = float(input("How much tip? 10/12/15. "))

per_person = (sum * (1 + (tip / 100))) / split

print(f"Each should pay {round(per_person, 2)}")