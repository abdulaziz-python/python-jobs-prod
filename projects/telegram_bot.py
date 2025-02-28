from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import CustomUser
import urllib.parse

User = get_user_model()

WEBSITE_DOMAIN = "https://8000-idx-course-1736610940535.cluster-blu4edcrfnajktuztkjzgyxzek.cloudworkstations.dev"

def start(update, context):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Ro'yxatdan o'tish", url=f"{WEBSITE_DOMAIN}/register/?telegram_id={user.id}")]
    ]
    
    custom_user = CustomUser.objects.filter(telegram_id=str(user.id)).first()
    if custom_user:
        login_url = f"{WEBSITE_DOMAIN}/telegram-login/?telegram_id={custom_user.telegram_id}"
        keyboard.append([InlineKeyboardButton("Saytga kirish", url=login_url)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Xush kelibsiz! Iltimos, tanlang:', reply_markup=reply_markup)

def handle_contact(update, context):
    contact = update.message.contact
    user, created = CustomUser.objects.get_or_create(
        telegram_id=str(contact.user_id),
        defaults={
            'username': f"telegram_{contact.user_id}",
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'is_active': True
        }
    )
    if created:
        update.message.reply_text("Ro'yxatdan o'tdingiz. Endi kompaniya nomini kiriting:")
        context.user_data['registration_step'] = 'company_name'
    else:
        login_url = f"{WEBSITE_DOMAIN}/telegram-login/?telegram_id={user.telegram_id}"
        keyboard = [[InlineKeyboardButton("Saytga kirish", url=login_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Siz allaqachon ro'yxatdan o'tgansiz. Saytga kirishingiz mumkin:", reply_markup=reply_markup)

def handle_message(update, context):
    if 'registration_step' in context.user_data:
        if context.user_data['registration_step'] == 'company_name':
            company_name = update.message.text
            user = CustomUser.objects.get(telegram_id=str(update.effective_user.id))
            user.company_name = company_name
            user.save()
            update.message.reply_text("Kompaniya nomi saqlandi. Ro'yxatdan o'tish yakunlandi.")
            
            login_url = f"{WEBSITE_DOMAIN}/telegram-login/?telegram_id={user.telegram_id}"
            keyboard = [[InlineKeyboardButton("Saytga kirish", url=login_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Endi siz saytga kirishingiz mumkin:", reply_markup=reply_markup)
            
            del context.user_data['registration_step']
    else:
        update.message.reply_text("Kechirasiz, men bu xabarni tushunmadim. /start buyrug'ini yuboring.")

