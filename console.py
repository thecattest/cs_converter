from converter import convert


if __name__ == '__main__':
    while 1:
        print('<Число> <исходная СИ> <целевая СИ>')
        try:
            try:
                n, base, target = list(input().split())
            except ValueError:
                raise ValueError("Не хватает аргументов")
            try:
                base, target = int(base), int(target)
            except ValueError:
                raise ValueError("СИ должна быть натуральным числом")

            print(convert(n, base, target))
        except Exception as e:
            print(f'Error: {e}')