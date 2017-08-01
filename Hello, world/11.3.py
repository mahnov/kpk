numBlocks = int(input('Сколько блоков звезд вам нужно? '))
for block in range(1, numBlocks+1):
    print('Блок = ', block)
    for line in range(1, block*2):
        for star in range(1, (block+line)*2):
            print('*', end='')
        print(' Строка = ', line, 'звезд = ', star)
    print()
