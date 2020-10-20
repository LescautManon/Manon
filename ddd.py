x = int(input())
k = 0
for i in range(2,x):
    if x % i == 0:
        print("Число сложное")
        k = 1
        break
if k == 0:
    print('Число простое')