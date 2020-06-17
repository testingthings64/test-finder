from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup ,User, Bot, Chat
from telegram.ext import Filters, MessageHandler, ConversationHandler, Updater, CommandHandler, CallbackQueryHandler
import logging
import database as db
import os


PORT = int(os.environ.get('PORT', 5000))
token = '981262545:AAGGFMJ_7i8lg_wCRuYQGCozJmxoRhAec10'
bot = Bot(token = token)

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
        [InlineKeyboardButton('جستجو بر اساس مهریه', callback_data = 'price_search')],
        [InlineKeyboardButton('آگهی های ذخیره شده', callback_data = 'saved_codes')]
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
        # [InlineKeyboardButton('جستجو بر اساس سن', callback_data = 'age_search'), 
        # InlineKeyboardButton('جستجو بر اساس نام', callback_data = 'name_search')]
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
        reg_female(update, context)

    #register male
    elif callback == 'register_male':
        reg_male(update, context)
    

    #return key
    elif callback == 'return_key':
        gender = db.get_gender(tel_id)[0]
        if gender == 'male':
            choices_male(update, context)
        elif gender == 'female':
            choices_female(update, context)

    #reserve code
    elif callback == 'reserve_code':
        reserve_code(update, context)

    #see photo
    elif callback.split('#')[0] == 'see_code':
        code = callback.split('#')[1]
        send_photo(code, tel_id)
        # print(update.callback_query)
    else:
        print(callback)
        not_exist(update, context)
    


def all_female(update, context):
    results = db.get_all_advertisements('female')
    if not results:
        text = """ 
            مشکلی پیش آمده، لطفا دوباره تلاش کنید
        """
    else:
        for res in results:
            text = f"""
                نام: {res[1]}
    سن: {res[2]}
    شهر: {res[3]}
    قد: {res[4]}
    وزن: {res[5]}
    مهریه: {res[6]}
    کد: {res[0]}#
    {res[8]}
                
            """
            ret = [
                [InlineKeyboardButton('درخواست این کد', callback_data = 'reserve_code')],
                [InlineKeyboardButton('مشاهده تصویر', callback_data = f'see_code#{res[0]}')],
                [InlineKeyboardButton('ذخیره آگهی', callback_data = f'save_code#{res[0]}')]
            ]
            ret_key = InlineKeyboardMarkup(ret)
            update.callback_query.message.reply_text(text = text, reply_markup = ret_key)

        return_key = [[InlineKeyboardButton('بازگشت', callback_data = 'return_key')]]
        update.callback_query.message.reply_text(text = 'برای بازگشت به منوی اصلی کلیک کنید', reply_markup = InlineKeyboardMarkup(return_key))


def send_photo(code, chat_id):
    bot.send_photo(chat_id = chat_id, photo =  open(f'photos/img_{code}.jpg', 'rb'))
    

def all_male(update, context):
    results = db.get_all_advertisements('male')
    if not results:
        text = """ 
            مشکلی پیش آمده، لطفا دوباره تلاش کنید
        """
    else:
        for res in results:
            text = res[1]
            ret = [
                [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
            ]
            ret_key = InlineKeyboardMarkup(ret)
            update.callback_query.message.reply_text(text = text, reply_markup = ret_key)


def reserve_code(update, context):
    text = 'برای درخواست این کد، لطفا به آی دی ادمین پیام بدهید'
    ret = [
        [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
    ]
    ret_key = InlineKeyboardMarkup(ret)
    update.callback_query.message.reply_text(text = text, reply_markup = ret_key)



def not_exist(update, context):
    ret = [
        [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
    ]
    ret_key = InlineKeyboardMarkup(ret)
    update.callback_query.edit_message_text(text = 'این مورد فعلا موجود نیست!', reply_markup = ret_key)













NAME, AGE, CITY, HEIGHT, WEIGHT, PRICE, NUMBER, CONTEXT, PHOTO = range(9)

data = {}

def reg_female(update, context):
    tel_id = update.callback_query.from_user.id
    exists = db.check_female_advertisement(tel_id)
    if not exists:
        data['tel_id'] = tel_id
        data['status'] = 'pending'
        text = """ 
            لطفا تمام اطلاعات خواسته شده را با دقت وارد نمایید.
            برای خروج از فرایند ثبت آگهی در هر مرحله، دستور  /cancel  را انتخاب نمایید.
            برای شروع ثبت نام دستور  /register  را انتخاب کنید
        """
    else:
        text = """ 
            شما قبلا ثبت آگهی کرده اید
        """
    ret = [
        [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
    ]
    ret_key = InlineKeyboardMarkup(ret)
    update.callback_query.edit_message_text(text = text, reply_markup = ret_key)


def reg_male(update, context):
    text = 'برای ثبت آگهی، لطفا به آی دی ادمین پیام بدهید'
    ret = [
        [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
    ]
    ret_key = InlineKeyboardMarkup(ret)
    update.callback_query.message.reply_text(text = text, reply_markup = ret_key)



def register(update, context):
    text = """ 
        لطفا نام و نام خانوادگی خود را وارد نمایید
    """
    update.message.reply_text(text)
    return NAME


def name(update, context):
    in_name = update.message.text
    data['name'] = in_name
    text = """ 
        لطفا سن خود را به صورت فقط عدد وارد نمایید
    """
    update.message.reply_text(text)
    return AGE
    

def age(update, context):
    in_age = update.message.text
    data['age'] = in_age
    text = """ 
        لطفا نام شهر محل زندگی خود را وارد نمایید
    """
    update.message.reply_text(text)
    return CITY


def city(update, context):
    in_city = update.message.text
    data['city'] = in_city
    text = """ 
        لطفا قد خود را به صورت فقط عدد بر حسب سانتی متر وارد نمایید

        مثال: 170
    """
    update.message.reply_text(text)
    return HEIGHT


def height(update, context):
    in_height = update.message.text
    data['height'] = in_height
    text = """ 
        لطفا وزن خود را به صورت فقط عدد بر حسب کیلوگرم وارد نمایید

        مثال: 70
    """
    update.message.reply_text(text)
    return WEIGHT


def weight(update, context):
    in_weight = update.message.text
    data['weight'] = in_weight
    text = """ 
        لطفا مهریه درخواستی خود برای یک ماه را بر حسب هزار تومان وارد نمایید

        مثال: هشت صد هزار تومان را 800 وارد نمایید
    """
    update.message.reply_text(text)
    return PRICE


def price(update, context):
    in_price = update.message.text
    data['price'] = in_price
    text = """ 
        لطفا شماره موبایل خود را جهت ارتباط با شما وارد نمایید
    """
    update.message.reply_text(text)
    return NUMBER


def number(update, context):
    in_number = update.message.text
    data['number'] = in_number
    text = """ 
        لطفا یک متن برای معرفی خود و نمایش به دیگران وارد نمایید
    """
    update.message.reply_text(text)
    return CONTEXT


def context(update, context):
    in_context = update.message.text
    data['context'] = in_context
    text = """ 
        لطفا یک عکس از خودتان جهت نمایش به دیگران ارسال نمایید
    """
    update.message.reply_text(text)
    return PHOTO


def photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    file_path = f'photos/img_{data["tel_id"]}.jpg'
    photo_file.download(file_path)
    # blob_form = convert_to_blob(file_path)
    # data['photo'] = blob_form
    res_reg = db.new_female_advertisement(data)
    if res_reg:
        text = """ 
            ثبت آگهی شما تکمیل شده است و پس از تایید توسط ادمین منتشر خواهد شد
        """
    else:
        text = """ 
            متاسفانه ثبت آگهی شما با خطا مواجه شد، لطفا دوباره تلاش کنید
        """
    ret = [
        [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
    ]
    ret_key = InlineKeyboardMarkup(ret)
    update.message.reply_text(text, reply_markup = ret_key)
    return ConversationHandler.END


def cancel(update, context):
    ret = [
        [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
    ]
    ret_key = InlineKeyboardMarkup(ret)
    text = """ 
        شما از فرایند ثبت آگهی خارج شدید
    """
    update.message.reply_text(text, reply_markup = ret_key)
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

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=token)
    updater.bot.setWebhook('https://safe-cove-63138.herokuapp.com/' + token)

    updater.idle()


# def convert_to_blob(file_name):
#     with open(file_name, 'rb') as file:
#         blob = file.read()
#     return blob


if __name__ == '__main__':
    main()

