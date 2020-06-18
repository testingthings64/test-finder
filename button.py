import main as m
import database as db
def btn(update, context):
    query = update.callback_query
    callback = query.data
    tel_id = update.callback_query.from_user.id
    query.answer()
    registered = db.check_user(tel_id)

    #gender buttons
    if callback == 'male' or 'female' and not registered:
        check = db.new_user(tel_id, callback)
        if check and callback == 'male':
            m.choices_male(update, context)
        elif check and callback == 'female':
            m.choices_female(update, context)

    #show all buttons
    elif callback == 'show_all_female':
        m.all_female(update, context)
    elif callback == 'show_all_male':
        m.all_male(update, context)

    #register female
    elif callback == 'register_female':
        m.reg_female(update, context)

    #register male
    elif callback == 'register_male':
        m.reg_male(update, context)
    

    #return key
    elif callback == 'return_key':
        gender = db.get_gender(tel_id)[0]
        if gender == 'male':
            m.choices_male(update, context)
        elif gender == 'female':
            m.choices_female(update, context)

    #reserve code
    elif callback == 'reserve_code':
        m.reserve_code(update, context)

    #see photo
    elif callback.split('#')[0] == 'see_photo':
        code = callback.split('#')[1]
        m.send_photo(code, tel_id)
        # print(update.callback_query)
    
    #save code
    elif callback.split('#')[0] == 'save_code':
        code = callback.split('#')[1]
        m.save_code(update, context, code, tel_id)

    #see code
    elif callback.split('#')[0] == 'see_code':
        code = callback.split('#')[1]
        m.see_code(update, context, code)

    #see save codes
    elif callback == 'saved_codes':
        m.saved_codes(update, context, tel_id)
    

    #age search
    elif callback == 'female_age_search':
        m.female_age_search(update,context)

    else:
        print(callback)
        m.not_exist(update, context)
    
