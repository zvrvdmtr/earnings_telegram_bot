from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import start_conversation, ticker, processing, skip_ticker, stop, error_handler
import settings
import re

PROXY = {'proxy_url': settings.SOCKS_URL,
         'urllib3_proxy_kwargs': {'username': settings.SOCKS_USERNAME,
                                  'password': settings.SOCKS_PASSWORD}}


def main():
    updater = Updater(settings.TELEGRAM_TOKEN, use_context=True, request_kwargs=PROXY)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_conversation)],
        states={
            'TICKER': [MessageHandler(Filters.regex(re.compile('^(Year|Week|Month|Day)$', re.IGNORECASE)), ticker)],
            'PROCESSING': [
                MessageHandler(Filters.text, processing),
                CommandHandler('skip', skip_ticker)
            ],
        },
        fallbacks=[CommandHandler("stop", stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
