from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup ,User, Bot, Chat
from telegram.ext import Filters, MessageHandler, ConversationHandler, Updater, CommandHandler, CallbackQueryHandler
import logging
import database as db
import button


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
        [InlineKeyboardButton('جستجو بر اساس سن', callback_data = 'female_age_search'), 
        InlineKeyboardButton('جستجو بر اساس نام', callback_data = 'female_name_search')],
        [InlineKeyboardButton('جستجو بر اساس مهریه', callback_data = 'price_search'),
        InlineKeyboardButton('جستجو بر اساس شهر', callback_data = 'famele_city_search')],
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



def all_female(update, context):
    results = db.get_all_advertisements('female')
    if not results:
        error_db(update, context)
    else:
        text = """ 
            لطفا روی کد مورد نظر کلیک کنید
        """
        key = []
        for res in results:
            key.append(code_btn(res[0]))
        key.append([InlineKeyboardButton('بازگشت', callback_data = 'return_key')])
        update.callback_query.edit_message_text(text = text, reply_markup = InlineKeyboardMarkup(key))


def send_photo(code, chat_id):
    bot.send_photo(chat_id = chat_id, photo =  open(f'photos/img_{code}.jpg', 'rb'))


def save_code(update, context, code, tel_id):

    res = db.new_save_code(code, tel_id)
    if res:
        text = 'آگهی مورد نظر با موفقیت ذخیره شد'
    else:
        text = 'آگهی مورد نظر قبلا ذخیره شده است'

    key = [[InlineKeyboardButton('بازگشت به کد', callback_data = f'see_code#{code}')]]
    update.callback_query.edit_message_text(text = text, reply_markup = InlineKeyboardMarkup(key))


def code_btn(res):
    res = db.get_btn(res)[0]
    btn = [InlineKeyboardButton(f"{res[1]} {res[0]}", callback_data = f"see_code#{res[0]}")]
    return btn

def see_code(update, context, code):
    
    res = db.get_code(code)
    if res:
        text = f"""
                    نام: {res[2]}
        سن: {res[3]}
        شهر: {res[4]}
        قد: {res[5]}
        وزن: {res[6]}
        مهریه: {res[7]}
        کد: {res[10]}#
        {res[9]}
                    
                """
        ret = [
            [InlineKeyboardButton('درخواست این کد', callback_data = 'reserve_code')],
            [InlineKeyboardButton('مشاهده تصویر', callback_data = f'see_photo#{res[10]}')],
            [InlineKeyboardButton('ذخیره آگهی', callback_data = f'save_code#{res[10]}')],
            # [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
        ]
        ret_key = InlineKeyboardMarkup(ret)
        update.callback_query.message.reply_text(text = text, reply_markup = ret_key)
    else:
        error_db(update, context)


# def saved_codes(update, context, tel_id):
#     results = db.get_saved_codes(tel_id)
#     if results:
#         key = show_btn(results)
#         text = """ 
#             لطفا روی کد مورد نظر کلیک کنید
#         """
#         key.append([InlineKeyboardButton('بازگشت', callback_data = 'return_key')])
#         update.callback_query.message.reply_text(text = text, reply_markup = InlineKeyboardMarkup(key))
#     else:
#         no_res(update,context)
    


def famele_city_search(update, context):
    text = 'لطفا نام استان مورد نظر خود را انتخاب کنید'
    cats = [
        [InlineKeyboardButton('اردبیل',callback_data='city#اردبیل'),
        InlineKeyboardButton('اصفهان',callback_data='city#اصفهان'),
        InlineKeyboardButton('آذربایجان غربی',callback_data='city#آذربایجان غربی'),
        InlineKeyboardButton('آذربایجان شرقی',callback_data='city#آذربایجان شرقی')],

        [InlineKeyboardButton('تهران',callback_data='city#تهران'),
        InlineKeyboardButton('بوشهر',callback_data='city#بوشهر'),
        InlineKeyboardButton('ایلام',callback_data='city#ایلام'),
        InlineKeyboardButton('البرز',callback_data='city#البرز')],

        [InlineKeyboardButton('خراسان شمالی',callback_data='city#خراسان شمالی'),
        InlineKeyboardButton('خراسان رضوی',callback_data='city#خراسان رضوی'),
        InlineKeyboardButton('خراسان جنوبی',callback_data='city#خراسان جنوبی'),
        InlineKeyboardButton('چهارمحال و بختیاری',callback_data='city#چهارمحال و بختیاری')],

        [InlineKeyboardButton('سیستان و بلوچستان',callback_data='city#سیستان و بلوچستان'),
        InlineKeyboardButton('سمنان',callback_data='city#سمنان'),
        InlineKeyboardButton('زنجان',callback_data='city#زنجان'),
        InlineKeyboardButton('خوزستان',callback_data='city#خوزستان')],

        [InlineKeyboardButton('فارس',callback_data='city#فارس'),
        InlineKeyboardButton('گلستان',callback_data='city#گلستان'),
        InlineKeyboardButton('کردستان',callback_data='city#کردستان'),
        InlineKeyboardButton('قم',callback_data='city#قم')],

        [InlineKeyboardButton('قزوین',callback_data='city#قزوین'),
        InlineKeyboardButton('کهگیلویه و بویراحمد',callback_data='city#کهگیلویه و بویراحمد'),
        InlineKeyboardButton('کرمانشاه',callback_data='city#کرمانشاه'),
        InlineKeyboardButton('کرمان',callback_data='city#کرمان')],
        
        [InlineKeyboardButton('مرکزی',callback_data='city#مرکزی'),
        InlineKeyboardButton('مازندران',callback_data='city#مازندران'),
        InlineKeyboardButton('لرستان',callback_data='city#لرستان'),
        InlineKeyboardButton('گیلان',callback_data='city#گیلان')],

        [InlineKeyboardButton('یزد',callback_data='city#یزد'),
        InlineKeyboardButton('همدان',callback_data='city#همدان'),
        InlineKeyboardButton('هرمزگان',callback_data='city#هرمزگان')]

    ]
    update.callback_query.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(cats, one_time_keyboard=True))





def all_male(update, context):
    results = db.get_all_advertisements('male')
    if not results:
        error_db(update, context)
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



def female_age_search(update,context):
    text = "بازه سنی مورد نظر خود را انتخاب نمایید"
    keys = [
        [InlineKeyboardButton('18 تا 30 سال', callback_data = 'age_range#1'),InlineKeyboardButton('30 تا 40 سال', callback_data = 'age_range#2')],
        [InlineKeyboardButton('40 تا 50 سال', callback_data = 'age_range#3'),InlineKeyboardButton('50 سال به بالا', callback_data = 'age_range#4')]
    ]
    ret_key = InlineKeyboardMarkup(keys)
    update.callback_query.edit_message_text(text = text, reply_markup = ret_key)


def price_search(update,context):
    text = "بازه مهریه مورد نظر خود را انتخاب نمایید"
    keys = [
        [InlineKeyboardButton('زیر 1 میلیون', callback_data = 'price_range#1'),InlineKeyboardButton('1 تا 1.5 میلیون', callback_data = 'price_range#2')],
        [InlineKeyboardButton('1.5 تا 2 میلیون', callback_data = 'price_range#3'),InlineKeyboardButton('بالای 2 میلیون', callback_data = 'price_range#4')]
    ]
    ret_key = InlineKeyboardMarkup(keys)
    update.callback_query.edit_message_text(text = text, reply_markup = ret_key)



# def age_range(update,context,age):
#     results = db.get_by_age(age)
#     if results:
#         text = """ 
#             لطفا روی کد مورد نظر کلیک کنید
#         """
#         keys = InlineKeyboardMarkup(show_btn(results))
#         update.callback_query.edit_message_text(text = text, reply_markup = keys)
#     else:
#         no_res(update,context)


# def price_range(update,context,price):
#     results = db.get_by_price(price)
#     if results:
#         text = """ 
#             لطفا روی کد مورد نظر کلیک کنید
#         """
#         keys = InlineKeyboardMarkup(show_btn(results))
#         update.callback_query.edit_message_text(text = text, reply_markup = keys)
#     else:
#         no_res(update,context)


def show_btn(results):
    key = []
    for res in results:
        key.append(code_btn(res[0]))
    key.append([InlineKeyboardButton('بازگشت', callback_data = 'return_key')])
    return key



def not_exist(update, context):
    ret = [
        [InlineKeyboardButton('بازگشت', callback_data = 'return_key')]
    ]
    ret_key = InlineKeyboardMarkup(ret)
    update.callback_query.edit_message_text(text = 'این مورد فعلا موجود نیست!', reply_markup = ret_key)


def show_results(update,context,results):
    if results:
        text = """ 
            لطفا روی کد مورد نظر کلیک کنید
        """
        keys = InlineKeyboardMarkup(show_btn(results))
        update.callback_query.edit_message_text(text = text, reply_markup = keys)
    else:
        no_res(update,context)











NAME, AGE, CITY, HEIGHT, WEIGHT, PRICE, NUMBER, CONTEXT, PHOTO = range(9)

data = {}

def reg_female(update, context):
    tel_id = update.callback_query.from_user.id
    exists = db.check_female_advertisement(tel_id)
    if not exists:
        text = """ 
            لطفا تمام اطلاعات خواسته شده را با دقت وارد نمایید.
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
    tel_id = update.message.chat.id
    data['tel_id'] = tel_id
    data['status'] = 'pending'
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
        لطفا نام استان محل زندگی خود را انتخاب نمایید
    """
    cats = [
        ['آذربایجان شرقی','آذربایجان غربی','اردبیل','اصفهان'],
        ['البرز','ایلام','بوشهر','تهران'],
        ['چهارمحال و بختیاری','خراسان جنوبی','خراسان رضوی','خراسان شمالی'],
        ['خوزستان','زنجان','سمنان','سیستان و بلوچستان'],
        ['فارس','قزوین','قم','کردستان'],
        ['کرمان','کرمانشاه','کهگیلویه و بویراحمد','گلستان'],
        ['گیلان','لرستان','	مازندران','	مرکزی'],
        ['هرمزگان','همدان','یزد']
    ]
    
    update.message.reply_text(text, reply_markup = ReplyKeyboardMarkup(cats, one_time_keyboard=True))
    return CITY


def city(update, context):
    in_city = update.message.text
    data['city'] = in_city
    text = """ 
        لطفا قد خود را به صورت فقط عدد بر حسب سانتی متر وارد نمایید

        مثال: 170
    """
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
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
    data['code_id'] = db.get_id(data['tel_id'])
    code_id = data['code_id']
    photo_file = update.message.photo[-1].get_file()
    file_path = f'photos/img_{code_id}.jpg'
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


def error_db(update, context):
    text = "مشکلی پیش آمده، لطفا دوباره تلاش کنید"
    ret_key = InlineKeyboardMarkup([[InlineKeyboardButton('بازگشت', callback_data = 'return_key')]])
    update.callback_query.message.reply_text(text = text, reply_markup = ret_key)


def no_res(update, context):
    text = "موردی وجود ندارد"
    ret_key = InlineKeyboardMarkup([[InlineKeyboardButton('بازگشت', callback_data = 'return_key')]])
    update.callback_query.message.reply_text(text = text, reply_markup = ret_key)


def main():
    updater = Updater(token, use_context = True)
    dis = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('register',register)],
        states = {
            NAME: [MessageHandler(Filters.text, name)],
            AGE: [MessageHandler(Filters.text, age)],
            CITY: [MessageHandler(Filters.regex('^(اصفهان|اردبیل|آذربایجان غربی|آذربایجان شرقی|تهران|بوشهر|ایلام|البرز|خراسان شمالی|سمنان|زنجان|خوزستان|کردستان|قم|قزوین|فارس|گلستان|کهگیلویه و بویراحمد|کرمانشاه|کرمان|مرکزی|مازندران|لرستان|گیلان|یزد|همدان|هرمزگان)$'), city)],
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
    dis.add_handler(CallbackQueryHandler(button.btn))

    updater.start_polling()

    updater.idle()


# def convert_to_blob(file_name):
#     with open(file_name, 'rb') as file:
#         blob = file.read()
#     return blob


if __name__ == '__main__':
    main()

