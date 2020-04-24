from converter import convert


if __name__ == '__main__':
    from logger import get_logger
    log = get_logger("log/console.log", "console")

    while 1:
        print('<Число> <исходная СИ> <целевая СИ>')
        inp = input()
        try:
            try:
                n, base, target = list(inp.split())
            except ValueError:
                raise ValueError("Не хватает аргументов")
            try:
                base, target = int(base), int(target)
            except ValueError:
                raise ValueError("СИ должна быть натуральным числом")

            converted = convert(n, base, target)
            log.info(f"[{inp}] = {converted}")
            print(converted)

        except Exception as e:
            log.error(f"{e} [{inp}]")
            print(f'Error: {e}')