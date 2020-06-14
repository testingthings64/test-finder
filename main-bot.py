from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Filters, MessageHandler, ConversationHandler, Updater, CommandHandler
import logging


token = '981262545:AAGGFMJ_7i8lg_wCRuYQGCozJmxoRhAec10'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


GENDER, AGE, CITY, PHOTO = range(4)


def start(update, context):
    keys = [['خانم', 'آقا']]

    update.message.reply_text(
        'سلام، به ربات دوستیاب خوش آمدید \n\n'
        'برای خارج شدن از روند ثبت نام دستور '
        '/cancel '
        'را انتخاب کنید \n\n'
        'برای شروع ابتدا جنسیت خود را انتخاب کنید',
    reply_markup = ReplyKeyboardMarkup(keys, one_time_keyboard = True))

    return GENDER


def gender(update, context):
    gender = update.message.text
    f_name = update.message.from_user.first_name
    text_gen = 'آقای' if gender == 'آقا' else 'خانم'
    text = f"{text_gen} {f_name} جنسیت شما با موفقیت ثبت شد، اکنون سن خود را وارد کنید"
    update.message.reply_text(text, reply_markup = ReplyKeyboardRemove())

    return AGE


def age(update, context):
    age = update.message.text
    update.message.reply_text(f'سن شما {age} سال با موفقیت ثبت شد. لطفا نام شهر خود را وارد کنید')
    return CITY


def city(update, context):
    city = update.message.text
    update.message.reply_text(f'نام شهر شما {city} سال با موفقیت ثبت شد. لطفا برای پروفایل خود یک عکس ارسال کنید \n\n'
    'برای رد شدن از این قسمت دستور '
    '/skip '
    'را انتخاب کنید')
    return PHOTO


def photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    update.message.reply_text('ثبت نام شما با موفقیت تکمیل شد. \n\n'
    'برای استفاده از امکانات ربات دکمه های زیر را انتخاب کنید')
    return ConversationHandler.END


def skip_photo(update, context):
    update.message.reply_text('ثبت نام شما با موفقیت تکمیل شد. \n\n'
    'برای استفاده از امکانات ربات دکمه های زیر را انتخاب کنید')
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('شما از روند ثبت نام خارج شدید', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    updater = Updater(token, use_context = True)
    dis = updater.dispatcher

    conversation = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            GENDER: [MessageHandler(Filters.regex('^(آقا|خانم)$'), gender)],
            AGE: [MessageHandler(Filters.text, age)],
            CITY: [MessageHandler(Filters.text, city)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    dis.add_handler(conversation)

    updater.start_polling()

    updater.idle()




if __name__ == '__main__':
    main()