from math import pow

#Решение
def solve(num):
    print('Кубическое число = ', round(pow(num, 1/3)))
    print()

#Решение без функции
def solve2(num):
    i = 1000
    while True:
        if (i*i*i > num):
            break
        if (i*i*i == num):
            print ('Кубический корень из числа %i = %i' %(num, i))
            break
        i += 1
    print()

#Главная функция
def main():
    print()
    print('Кубическое число')
    print()
    solve(996703628669)
    solve(1011443374872)
    solve2(996703628669)
    solve2(1011443374872)

main()
