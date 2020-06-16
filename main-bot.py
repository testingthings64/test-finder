from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup ,User
from telegram.ext import Filters, MessageHandler, ConversationHandler, Updater, CommandHandler, CallbackQueryHandler
import logging
import database as db


token = '981262545:AAGGFMJ_7i8lg_wCRuYQGCozJmxoRhAec10'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

GENDER = range(1)


def start(update, context):
    tel_id = update.message.chat.id
    if not db.check_user(tel_id):
        keys = [
            [InlineKeyboardButton('آقا', callback_data = 'male'), InlineKeyboardButton('خانم', callback_data = 'female')]
        ]
        update.message.reply_text(
            'سلام، به ربات دوستیاب خوش آمدید \n\n'
            'برای شروع ابتدا جنسیت خود را انتخاب کنید',
        reply_markup = InlineKeyboardMarkup(keys, one_time_keyboard=True))
    else:
        gender = db.get_gender(tel_id)[0]
        if gender == 'male':
            choices_male(update, context, False)
        elif gender == 'female':
            choices_female(update, context, False)


# def gender(update, context):
#     gender = update.message.text
#     f_name = update.message.from_user.first_name
#     text_gen = 'آقای' if gender == 'آقا' else 'خانم'
#     text = f"{text_gen} {f_name} جنسیت شما با موفقیت ثبت شد، برای استفاده از خدمات دستور  start/ را انتخاب کنید "
#     update.message.reply_text(text, reply_markup = ReplyKeyboardRemove())


def choices_male(update, context, button = True):
    keyboards = [
        [InlineKeyboardButton('مشاهده همه آگهی های خانم', callback_data = 'show_all_female')],
        [InlineKeyboardButton('ثبت آگهی جدید', callback_data = 'new_advertisment')],
        [InlineKeyboardButton('جستجو بر اساس سن', callback_data = 'age_search'), 
        InlineKeyboardButton('جستجو بر اساس نام', callback_data = 'name_search')],
        [InlineKeyboardButton('جستجو بر اساس مهریه', callback_data = 'price_search')]
    ]
    show_keys = InlineKeyboardMarkup(keyboards, one_time_keyboard=True)
    if button:
        update.callback_query.edit_message_text(text = 'لطفا یکی از گزینه های زیر را انتخاب کنید', reply_markup = show_keys)
    else:
        update.message.reply_text(text = 'لطفا یکی از گزینه های زیر را انتخاب کنید', reply_markup = show_keys)


def choices_female(update, context, button = True):
    keyboards = [
        [InlineKeyboardButton('مشاهده همه آگهی های آقا', callback_data = 'show_all_male')],
        [InlineKeyboardButton('ثبت آگهی جدید', callback_data = 'new_advertisment')],
        [InlineKeyboardButton('جستجو بر اساس سن', callback_data = 'age_search'), 
        InlineKeyboardButton('جستجو بر اساس نام', callback_data = 'name_search')]
    ]
    show_keys = InlineKeyboardMarkup(keyboards, one_time_keyboard=True)
    if button:
        update.callback_query.edit_message_text(text = 'لطفا یکی از گزینه های زیر را انتخاب کنید', reply_markup = show_keys)
    else:
        update.message.reply_text(text = 'لطفا یکی از گزینه های زیر را انتخاب کنید', reply_markup = show_keys)


def buttons(update, context):
    query = update.callback_query
    callback = query.data
    tel_id = update.callback_query.from_user.id
    query.answer()
    registered = db.check_user(tel_id)
    if callback == 'male' or 'female' and not registered:
        check = db.new_user(tel_id, callback)
        if check and callback == 'male':
            choices_male(update, context)
        elif check and callback == 'female':
            choices_female(update, context)
    elif callback == 'show_all_female':
        all_female(update, context)
    elif callback == 'show_all_male':
        all_male(update, context)
    else:
        not_exist(update, context)
    
# 3 name,age,city,height,weight,price,number,context,photo,code,status
def all_female(update, context):
    results = db.get_all_advertisments('female')
    for res in results:
        text = f"""
            نام: {res[2]}
سن: {res[3]}
شهر: {res[4]}
قد: {res[5]}
وزن: {res[6]}
مهریه: {res[7]}
کد: {res[11]}
{res[9]}
            
        """
        update.callback_query.message.reply_text(text = text)

def all_male(update, context):
    results = db.get_all_advertisments('male')
    print(results)


def not_exist(update, context):
    update.callback_query.edit_message_text(text = 'این مورد فعلا موجود نیست!')



def main():
    updater = Updater(token, use_context = True)
    dis = updater.dispatcher


    dis.add_handler(CommandHandler('start',start))

    dis.add_handler(CallbackQueryHandler(buttons))

    updater.start_polling()

    updater.idle()




if __name__ == '__main__':
    main()

