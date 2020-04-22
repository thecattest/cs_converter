import sys
sys.path.append("..")

from converter import convert

import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
try:
    from tg_token import TOKEN
except ImportError:
    print('Файл с токеном не найден')
    TOKEN = ''


def start(update, context):
    update.message.reply_text("Привет! Конвертирую числа из любых систем исчисления в любые.\n"
                              "Для справки отправь /help\n")


def help(update, context):
    update.message.reply_text("Отправь сообщение формата\n"
                              "<Число> <Исходная СИ> <Целевая СИ>\n"
                              "и получи результат")


def credits(update, context):
    update.message.reply_text("Автор: @thecattest\n"
                              "Source: github.com/ilya-vodopyanov/cs_converter")


def stop(update, context):
    update.message.reply_text("Ну допустим стоп...")


def convert_from_message(update, context):
    message = update.message.text
    try:
        n, base, target = message.split()
        try:
            base, target = int(base), int(target)
        except ValueError:
            raise ValueError("СИ должна быть натуральным числом")
        else:
            result = convert(n, base, target)
            if len(result) > 5:
                answer = ''
                for n in range(0, len(result), 3):
                    answer += ''.join(list(list(result)[n:n + 3])) + ' '
                # answer = answer[::-1]
            else:
                answer = result
    except Exception as e:
        update.message.reply_text(f'Ошибка: {e}')
        help(update, context)
    else:
        update.message.reply_text(answer)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('credits', credits))
    dp.add_handler(MessageHandler(Filters.regex(r'[\da-zA-z]+\s+\d+\s+\d+'), convert_from_message))
    dp.add_handler(MessageHandler(Filters.text, help))

    try:
        updater.start_polling()
        updater.idle()
    except telegram.error.TelegramError:
        print("Ошибка. Видимо, ваш провайдер блокирует запросы.")
        exit(1)


if __name__ == '__main__':
    main()
