numBlocks = int(input('Сколько блоков со звездами требуется?'))
numLines = int(input('Сколько строк со звездами требуется?'))
numStars = int(input('Сколько звезд должно быть в строке?'))
for blocks in range (0, numBlocks):
    for line in range(0, numLines):
        for star in range(0, numStars):
            print('*', end=' ')
        print()
    print()
