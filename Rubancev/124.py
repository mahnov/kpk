from itertools import permutations

def solve(puzzle):
    n_var = 0 # Число вариантов
    # составляем список слов:
    words = [w for w in puzzle.split() if w.isalpha()]
    print(words)
    # множество первых букв, которые не могут равняться нулю:
    first_chars = {w[0] for w in words}
    print(first_chars)
    # множество остальных букв, которые могут равняться нулю:
    other_chars = {a for a in ''.join(words) if a not in first_chars}
    print(other_chars)
    # список всех букв:
    all_chars = [ord(c) for c in first_chars] + [ord(c) for c in other_chars]
    print(all_chars)

    # число разных букв не должно превыщать 10:
    if (len(all_chars) > 10):
        print('Слишком много цифр!')
        return 0

    # генерируем все возможные перестанови из len(chars)
    for perm in permutations('0123456789', len(all_chars)):
        # первой цифрой не может быть нуль:
        if '0' not in perm[:len(first_chars)]:
            # составляем числовое выражение, заменяя буквы цифрами:
            equation = puzzle.translate(dict(zip(all_chars, perm)))
            #print(equation)
            # если оно верное,
            if eval(equation):
                # то печатаем очередное решение:
                n_var += 1
                print('Вариант #', n_var)
                print ('\n'.join((puzzle, equation)))
    return n_var

# ГЛАВНАЯ ФУНКЦИЯ
def main():
    print()
    print('Решаем числовой ребус')
    print()
    #puzzle = 'ЛОБ + ТРИ == САМ'
    #puzzle = 'УА * ВБГ == ИЯ * ЖДА'
    puzzle = 'IMPRESARIO + PARATROOPS + TETRAMETER == ASPIRATION'
    nVar = solve(puzzle)
    print('Найдены все варианты решения -', nVar)
    print()
main()
