friends = []
print('Введите 5 имен. После каждого нажимайте Enter')
for i in range(5):
    friends.append(str(input()))
print('Твои друзья:')
for i in friends:
    print(i, end=', ')
print('Отсортированный:')
for i in friends:
    print(i, end=', ')
friends.sort()
