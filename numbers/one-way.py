N = 4
m1 = None
for i in range(N):
    x = int(input())
    if x%2 == 0:
        if m1 == None or x > m1:
            m1 = x
if m1 != None:
    print('Максимальное четное', m1)
else:
    print('Четных не было!')
