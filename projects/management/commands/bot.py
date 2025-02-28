from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from projects.telegram_bot import start, handle_message, handle_contact

class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.contact, handle_contact))
        dp.add_handler(MessageHandler(Filters.text, handle_message))

        updater.start_polling()
        self.stdout.write(self.style.SUCCESS('Telegram bot is running...'))
        updater.idle()

