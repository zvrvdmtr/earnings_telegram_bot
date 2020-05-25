from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import settings
from services import finnhub_connection

PROXY = {'proxy_url': settings.SOCKS_URL,
         'urllib3_proxy_kwargs': {'username': settings.SOCKS_USERNAME,
                                  'password': settings.SOCKS_PASSWORD}}


PERIOD = ['Year', 'Month', 'Week', 'Day']


def start(update, context):
    replies = [PERIOD]
    update.message.reply_text('Choose wisely', reply_markup=ReplyKeyboardMarkup(replies, one_time_keyboard=True))
    return 'TICKER'


def ticker(update, context):
    context.user_data[update.message.from_user.id] = {'period': settings.PERIODS[update.message.text.upper()]}
    update.message.reply_text('Enter ticker. Or send /skip.', reply_markup=ReplyKeyboardRemove())
    return 'PROCESSING'


def skip_ticker(update, context):
    return 'PROCESSING'


def processing(update, context):
    context.user_data[update.message.from_user.id].update({'ticker': update.message.text})
    update.message.reply_text('Start processing. Wait.')
    finnhub_connection(period=context.user_data[update.message.from_user.id]['period'])
    update.message.reply_text('Your report is ready.')
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text('Conversation end', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    updater = Updater(settings.TELEGRAM_TOKEN, use_context=True, request_kwargs=PROXY)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            'TICKER': [MessageHandler(Filters.regex('^(Year|Week|Month|Day)$'), ticker)],
            'PROCESSING': [
                MessageHandler(Filters.text, processing),
                CommandHandler('skip', skip_ticker)
            ],
        },
        fallbacks=[CommandHandler("stop", stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
