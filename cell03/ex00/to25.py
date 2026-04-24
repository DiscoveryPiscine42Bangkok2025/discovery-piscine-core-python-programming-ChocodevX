print("enter number less than 25 : ")
x = int(input())
if x < 25:
    while x < 25:
        x += 1
        print("inside the loop, my variable is: ", x)
else:
    print("The number is greater than or equal to 25")