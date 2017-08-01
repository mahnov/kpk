x = int(input())
n = 0
s = 0
p = 1
while x:
    digit = x%10
    n += 1
    s += digit
    p *= digit
    x //= 10
print('Количество цифр', n)
print('Сумма цифр', s)
print('Произведение цифр', p)
print('Среднее арифметическое цифр', s/n)
