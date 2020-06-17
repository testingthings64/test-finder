from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup ,User
from telegram.ext import Filters, MessageHandler, ConversationHandler, Updater, CommandHandler, CallbackQueryHandler
import logging
import database as db


token = '981262545:AAGGFMJ_7i8lg_wCRuYQGCozJmxoRhAec10'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


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



def choices_male(update, context, button = True):
    keyboards = [
        [InlineKeyboardButton('مشاهده همه آگهی های خانم', callback_data = 'show_all_female')],
        [InlineKeyboardButton('ثبت آگهی جدید', callback_data = 'register_male')],
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
        [InlineKeyboardButton('ثبت آگهی جدید', callback_data = 'register_female')],
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

    #gender buttons
    if callback == 'male' or 'female' and not registered:
        check = db.new_user(tel_id, callback)
        if check and callback == 'male':
            choices_male(update, context)
        elif check and callback == 'female':
            choices_female(update, context)

    #show all buttons
    elif callback == 'show_all_female':
        all_female(update, context)
    elif callback == 'show_all_male':
        all_male(update, context)

    #register female
    elif callback == 'register_female':
        start_reg(update, context)

    #return key
    elif callback == 'return_key':
        gender = db.get_gender(tel_id)[0]
        if gender == 'male':
            choices_male(update, context)
        elif gender == 'female':
            choices_female(update, context)


    else:
        print(callback)
        not_exist(update, context)
    


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


NAME, AGE, CITY, HEIGHT, WEIGHT, PRICE, NUMBER, CONTEXT, PHOTO = range(9)

def start_reg(update, context):
    text = """ 
        لطفا تمام اطلاعات خواسته شده را با دقت وارد نمایید.
        برای خروج از فرایند ثبت آگهی در هر مرحله، دستور  /cancel  را انتخاب نمایید.
        برای شروع ثبت نام دستور  /register  را انتخاب کنید
    """
    ret = [
        [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
    ]
    ret_key = InlineKeyboardMarkup(ret)
    update.callback_query.message.reply_text(text, reply_markup = ret_key)


def register(update, context):
    text = """ 
        لطفا نام و نام خانوادگی خود را وارد نمایید
    """
    update.message.reply_text(text)
    return NAME


def name(update, context):
    in_name = update.message.text
    print(in_name)
    text = """ 
        لطفا سن خود را به صورت فقط عدد وارد نمایید
    """
    update.message.reply_text(text)
    return AGE
    

def age(update, context):
    in_age = update.message.text
    print(in_age)
    text = """ 
        لطفا نام شهر محل زندگی خود را وارد نمایید
    """
    update.message.reply_text(text)
    return CITY


def city(update, context):
    in_city = update.message.text
    print(in_city)
    text = """ 
        لطفا قد خود را به صورت فقط عدد بر حسب سانتی متر وارد نمایید

        مثال: 170
    """
    update.message.reply_text(text)
    return HEIGHT


def height(update, context):
    in_height = update.message.text
    print(in_height)
    text = """ 
        لطفا وزن خود را به صورت فقط عدد بر حسب کیلوگرم وارد نمایید

        مثال: 70
    """
    update.message.reply_text(text)
    return WEIGHT


def weight(update, context):
    in_weight = update.message.text
    print(in_weight)
    text = """ 
        لطفا مهریه درخواستی خود برای یک ماه را بر حسب هزار تومان وارد نمایید

        مثال: هشت صد هزار تومان را 800 وارد نمایید
    """
    update.message.reply_text(text)
    return PRICE


def price(update, context):
    in_price = update.message.text
    print(in_price)
    text = """ 
        لطفا شماره موبایل خود را جهت ارتباط با شما وارد نمایید
    """
    update.message.reply_text(text)
    return NUMBER


def number(update, context):
    in_number = update.message.text
    print(in_number)
    text = """ 
        لطفا یک متن برای معرفی خود و نمایش به دیگران وارد نمایید
    """
    update.message.reply_text(text)
    return CONTEXT


def context(update, context):
    in_context = update.message.text
    print(in_context)
    text = """ 
        لطفا یک عکس از خودتان جهت نمایش به دیگران ارسال نمایید
    """
    update.message.reply_text(text)
    return PHOTO


def photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    text = """ 
        ثبت نام شما تکمیل و آگهی شما ثبت شده است و پس از تایید توسط ادمین منتشر خواهد شد
    """
    update.message.reply_text(text)
    return ConversationHandler.END


def cancel(update, context):
    text = """ 
        شما از فرایند ثبت آگهی خارج شدید
    """
    update.message.reply_text(text)
    return ConversationHandler.END



def main():
    updater = Updater(token, use_context = True)
    dis = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('register',register)],
        states = {
            NAME: [MessageHandler(Filters.text, name)],
            AGE: [MessageHandler(Filters.text, age)],
            CITY: [MessageHandler(Filters.text, city)],
            HEIGHT: [MessageHandler(Filters.text, height)],
            WEIGHT: [MessageHandler(Filters.text, weight)],
            PRICE: [MessageHandler(Filters.text, price)],
            NUMBER: [MessageHandler(Filters.text, number)],
            CONTEXT: [MessageHandler(Filters.text, context)],
            PHOTO: [MessageHandler(Filters.photo, photo)]
        },
        fallbacks = [CommandHandler('cancel',cancel)]
    )

    dis.add_handler(CommandHandler('start',start))
    dis.add_handler(conv_handler)
    dis.add_handler(CallbackQueryHandler(buttons))

    updater.start_polling()

    updater.idle()




if __name__ == '__main__':
    main()

