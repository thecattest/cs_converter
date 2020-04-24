import sys
sys.path.append("..")

from converter import convert

import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
try:
    from tg_token import TOKEN
except ImportError:
    print('Файл с токеном не найден')
    TOKEN = ''


def log(message):
    from_user = message.from_user
    user = f"({from_user.first_name} {from_user.last_name} @{from_user.username})"

    text = message.text

    messages_log.info(f"{user} \"{text}\"")


def start(update, context):
    log(update.message)
    update.message.reply_text("Привет! Конвертирую числа из любых систем исчисления в любые.\n"
                              "Для справки отправь /help\n")


def help(update, context):
    log(update.message)
    update.message.reply_text("Отправь сообщение формата\n"
                              "<Число> <Исходная СИ> <Целевая СИ>\n"
                              "и получи результат")


def credits(update, context):
    log(update.message)
    update.message.reply_text("Автор: @thecattest\n"
                              "Source: github.com/ilya-vodopyanov/cs_converter")


def stop(update, context):
    log(update.message)
    update.message.reply_text("Ну допустим стоп...")


def convert_from_message(update, context):
    log(update.message)
    message_text = update.message.text
    try:
        n, base, target = message_text.split()
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
            else:
                answer = result
    except Exception as e:
        answer_log.error(f"{e} [{message_text}]")
        update.message.reply_text(f'Ошибка: {e}')
        help(update, context)
    else:
        answer_log.info(f"[{message_text}] = {answer}")
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
    from logger import get_logger

    answer_log = get_logger("log/bot/answers.log", "bot")
    messages_log = get_logger("log/bot/messages.log", "bot")

    main()
